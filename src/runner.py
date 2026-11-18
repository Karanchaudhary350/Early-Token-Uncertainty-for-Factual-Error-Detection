"""Prompt 09: deterministic, resumable TruthfulQA baseline generation.

No correctness labels or AUROC/AUPRC are produced here.
"""
import csv
import hashlib
import importlib.metadata
import json
import os
import platform
import random
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from uncertainty import FEATURES, compute_features

SEED = 20261113
MODEL_ID = 'Qwen/Qwen2.5-0.5B-Instruct'
MODEL_SHA = '7ae557604adf67be50417f59c2c2f167def9a775'
DATA_SHA = 'b8d8ef1e12f98b4f2a9f47abc9765da0640b182b6c5d9b92f0c1a1f2f1e02e5c'
TEMPLATE_SHA = 'cd8e9439f0570856fd70470bf8889ebd8b5d1107207f67a5efb46e342330527f'
QUESTION_TEMPLATE = 'Answer the following question briefly and factually. Give only the answer, without explanation.\n\nQuestion: {question}'


def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for block in iter(lambda: f.read(1024*1024), b''):
            h.update(block)
    return h.hexdigest()


def atomic_json(path, data):
    path = Path(path)
    temp = path.with_suffix(path.suffix + '.tmp')
    temp.write_text(json.dumps(data, indent=2, ensure_ascii=False, default=str)+'\n', encoding='utf-8')
    os.replace(temp, path)


def read_records(path):
    if not Path(path).exists():
        return []
    records = []
    with open(path, encoding='utf-8') as f:
        for i, line in enumerate(f, 1):
            if line.strip():
                try:
                    records.append(json.loads(line))
                except json.JSONDecodeError as e:
                    raise RuntimeError(f'Invalid JSONL line {i}; restore file before resuming: {e}')
    return records


def validate_inputs(data_path, sample_path):
    if sha256(data_path) != DATA_SHA:
        raise RuntimeError('TruthfulQA source SHA256 mismatch. Stop: dataset changed.')
    data = pd.read_csv(data_path).fillna('')
    sample = pd.read_csv(sample_path)
    if len(data) != 790 or len(sample) != 100:
        raise RuntimeError('Expected frozen 790-row source and 100-question sample.')
    if sample['dataset_row_index'].duplicated().any():
        raise RuntimeError('Duplicate sampled question IDs')
    if sample['sample_position'].tolist() != list(range(100)):
        raise RuntimeError('Sample position order changed')
    if sample['partition'].tolist() != ['pilot']*20 + ['held_out']*80:
        raise RuntimeError('Frozen pilot/held-out partitions changed')
    for r in sample.itertuples(index=False):
        idx = int(r.dataset_row_index)
        if idx < 0 or idx >= len(data) or str(data.iloc[idx]['Question']) != str(r.question):
            raise RuntimeError(f'Frozen question mismatch at row {idx}')
    expected = random.Random(SEED).sample(range(len(data)), 100)
    if sample['dataset_row_index'].astype(int).tolist() != expected:
        raise RuntimeError('Frozen sample does not match protocol sampling seed')
    return data, sample


def load_model():
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, revision=MODEL_SHA)
    template_sha = hashlib.sha256(str(tokenizer.chat_template).encode()).hexdigest()
    if template_sha != TEMPLATE_SHA:
        raise RuntimeError('Chat template hash mismatch; do not silently change prompts.')
    model = AutoModelForCausalLM.from_pretrained(MODEL_ID, revision=MODEL_SHA, torch_dtype=torch.float32)
    model.eval()
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model.to(device)
    return tokenizer, model, device


def generate_one(question, tokenizer, model, device):
    messages = [{'role': 'user', 'content': QUESTION_TEMPLATE.format(question=question)}]
    encoded = tokenizer.apply_chat_template(messages, tokenize=True, add_generation_prompt=True, return_tensors='pt')
    input_ids = (encoded['input_ids'] if hasattr(encoded, 'keys') else encoded).to(device)
    attention_mask = torch.ones_like(input_ids)
    with torch.inference_mode():
        out = model.generate(
            input_ids=input_ids, attention_mask=attention_mask,
            do_sample=False, num_beams=1, max_new_tokens=64,
            return_dict_in_generate=True, output_scores=True,
            output_logits=True, use_cache=False,
            pad_token_id=tokenizer.eos_token_id,
        )
    generated_ids = out.sequences[0, input_ids.shape[1]:].tolist()
    if len(out.logits) != len(generated_ids):
        raise RuntimeError('Raw generation logits count does not match generated tokens')
    special = set(tokenizer.all_special_ids)
    tokens = []
    scored = []
    for step, (token_id, raw_logits) in enumerate(zip(generated_ids, out.logits)):
        log_probs = torch.log_softmax(raw_logits[0].float(), dim=-1)
        nll = -float(log_probs[int(token_id)].item())
        if not np.isfinite(nll):
            raise RuntimeError('Nonfinite NLL at step '+str(step))
        is_special = int(token_id) in special
        tokens.append({'step':step,'token_id':int(token_id),
                       'token_text':tokenizer.convert_ids_to_tokens(int(token_id)),
                       'is_special':bool(is_special),'nll':nll if not is_special else None})
        if not is_special:
            scored.append(nll)
    features = compute_features(scored)
    eos_ids = getattr(model.generation_config, 'eos_token_id', tokenizer.eos_token_id)
    if isinstance(eos_ids, int): eos_ids = [eos_ids]
    stop = 'eos' if generated_ids and generated_ids[-1] in set(eos_ids or []) else ('max_new_tokens' if len(generated_ids)==64 else 'other')
    answer_ids = [i for i in generated_ids if i not in special]
    answer = tokenizer.decode(answer_ids, skip_special_tokens=True)
    return {
        'answer':answer,'generated_token_ids':generated_ids,'tokens':tokens,
        'scored_token_count':len(scored),'features':features,
        'finish_reason':stop,
        'invalid_reason':'zero_scored_tokens' if not scored else None,
    }


def export_csv(jsonl_path, csv_path, sample):
    rows = read_records(jsonl_path)
    if not rows:
        return
    positions = {int(r.sample_position):r for r in sample.itertuples(index=False)}
    columns = ['sample_position','dataset_row_index','partition','question','answer',
               'scored_token_count','generated_token_count','finish_reason','invalid_reason',*FEATURES]
    with open(csv_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        for r in sorted(rows, key=lambda x:x['sample_position']):
            pos = int(r['sample_position'])
            original = positions[pos]
            if int(original.dataset_row_index) != int(r['dataset_row_index']):
                raise RuntimeError('Resume record row mismatch')
            writer.writerow({
                'sample_position':pos,'dataset_row_index':r['dataset_row_index'],
                'partition':r['partition'],'question':r['question'], 'answer':r['answer'],
                'scored_token_count':r['scored_token_count'],
                'generated_token_count':len(r['generated_token_ids']),
                'finish_reason':r['finish_reason'],'invalid_reason':r['invalid_reason'],
                **r['features']
            })


def run(data_path, sample_path, output_dir, limit=None):
    """Run next `limit` unfinished examples (None = finish all 100)."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    data, sample = validate_inputs(data_path, sample_path)
    jsonl = output_dir/'generations.jsonl'
    old = read_records(jsonl)
    seen = set()
    for r in old:
        pos = int(r['sample_position'])
        if pos in seen or pos not in set(sample.sample_position.astype(int)):
            raise RuntimeError('Duplicate/unknown saved sample_position')
        original = sample.iloc[pos]
        if int(r['dataset_row_index']) != int(original['dataset_row_index']) or r['question'] != original['question']:
            raise RuntimeError('Saved records do not match frozen sample')
        if r.get('model_id') != MODEL_ID or r.get('model_revision_sha') != MODEL_SHA or r.get('scoring_mode') != 'float32_raw_generation_logits_no_cache':
            raise RuntimeError('Saved records generated under different model/scoring settings')
        seen.add(pos)
    pending = [r for r in sample.itertuples(index=False) if int(r.sample_position) not in seen]
    if limit is not None:
        if limit < 0: raise ValueError('limit must be >=0 or None')
        pending = pending[:limit]
    manifest_path = output_dir/'run_manifest.json'
    if manifest_path.exists():
        prior = json.loads(manifest_path.read_text())
        if prior.get('dataset_sha256') != DATA_SHA or prior.get('sample_sha256') != sha256(sample_path) or prior.get('model_revision_sha') != MODEL_SHA:
            raise RuntimeError('Existing output manifest incompatible with frozen inputs')
    else:
        versions = {}
        for name in ['torch','transformers','pandas','numpy','accelerate']:
            try: versions[name] = importlib.metadata.version(name)
            except importlib.metadata.PackageNotFoundError: versions[name] = None
        atomic_json(manifest_path, {
            'started_utc':datetime.now(timezone.utc).isoformat(),
            'python':sys.version,'platform':platform.platform(),'gpu':torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
            'model_id':MODEL_ID,'model_revision_sha':MODEL_SHA,'model_dtype':'float32',
            'dataset_sha256':DATA_SHA,'sample_sha256':sha256(sample_path),
            'seed':SEED,'packages':versions,
            'generation':{'do_sample':False,'num_beams':1,'max_new_tokens':64,'use_cache':False,'output_logits':True},
            'scoring_mode':'float32_raw_generation_logits_no_cache',
            'protocol_amendment':'Prompt08 v4 validated raw logits with float32 and use_cache=False; Prompt09 adopts this for consistency.',
            'no_correctness_labels':True,'no_performance_metrics':True
        })
    if pending:
        random.seed(SEED); np.random.seed(SEED); torch.manual_seed(SEED)
        if torch.cuda.is_available(): torch.cuda.manual_seed_all(SEED)
        tokenizer, model, device = load_model()
        for n, item in enumerate(pending, 1):
            pos = int(item.sample_position)
            row = generate_one(str(item.question), tokenizer, model, device)
            record = {
                'sample_position':pos,'dataset_row_index':int(item.dataset_row_index),
                'partition':str(item.partition),'question':str(item.question),
                'model_id':MODEL_ID,'model_revision_sha':MODEL_SHA,
                'scoring_mode':'float32_raw_generation_logits_no_cache',
                **row
            }
            # Flush each completed record so Colab interruptions do not lose earlier work.
            with open(jsonl, 'a', encoding='utf-8') as f:
                f.write(json.dumps(record, ensure_ascii=False, allow_nan=False)+'\n')
                f.flush(); os.fsync(f.fileno())
            print(f'[{n}/{len(pending)}] saved position={pos} partition={item.partition} scored_tokens={row["scored_token_count"]}', flush=True)
    export_csv(jsonl, output_dir/'features.csv', sample)
    done = read_records(jsonl)
    stats = {'updated_utc':datetime.now(timezone.utc).isoformat(),
             'completed':len(done),'expected':len(sample),
             'pilot_completed':sum(r['partition']=='pilot' for r in done),
             'held_out_completed':sum(r['partition']=='held_out' for r in done),
             'zero_scored_tokens':sum(r['scored_token_count']==0 for r in done),
             'length_lt_5':sum(r['scored_token_count']<5 for r in done),
             'length_lt_10':sum(r['scored_token_count']<10 for r in done),
             'complete':len(done)==len(sample),
             'labels_generated':False,'performance_metrics_generated':False}
    atomic_json(output_dir/'progress.json', stats)
    return stats

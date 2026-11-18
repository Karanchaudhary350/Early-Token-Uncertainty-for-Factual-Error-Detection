import argparse,csv,json,zipfile,math,hashlib
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.metrics import roc_auc_score,average_precision_score,roc_curve,precision_recall_curve
FEATURES=['first_1_mean_nll','first_5_mean_nll','first_10_mean_nll','full_mean_nll','full_max_surprise']
def load(zippath,annotations):
 with zipfile.ZipFile(zippath) as z:
  feat=list(csv.DictReader(z.read('features.csv').decode().splitlines()))
  gen=[json.loads(x) for x in z.read('generations.jsonl').decode().splitlines() if x.strip()]
  manifest=json.loads(z.read('run_manifest.json'))
 with open(annotations,newline='',encoding='utf-8') as f: ann=list(csv.DictReader(f))
 return feat,gen,ann,manifest
def validate(feat,gen,ann):
 assert len(feat)==len(gen)==len(ann)==100,'Expected 100 records in each input'
 def unique(rows,k):
  d={str(x[k]):x for x in rows};assert len(d)==len(rows),f'Duplicate {k}';return d
 f=unique(feat,'sample_position');g=unique(gen,'sample_position');a=unique(ann,'question_id')
 assert f.keys()==g.keys()==a.keys(),'ID mismatch'
 for i in f:
  x,y,z=f[i],g[i],a[i]
  assert x['question']==z['question']==y['question'],f'Question mismatch {i}'
  assert ''.join(x['answer'].split())==''.join(z['generated_answer'].split()),f'Substantive answer mismatch {i}'
  assert x['partition']==z['split'],f'Split mismatch {i}'
  assert x['partition'] in ('pilot','held_out')
  for k in FEATURES:
   if x[k]:assert math.isfinite(float(x[k])),f'Nonfinite {k} {i}'
  assert z['label'] in ('0','1','U',''),f'Unexpected label {i}'
 return f,a

def writecsv(p,rows,cols):
 with open(p,'w',newline='',encoding='utf-8') as h:
  w=csv.DictWriter(h,fieldnames=cols);w.writeheader();w.writerows(rows)

def main():
 p=argparse.ArgumentParser();p.add_argument('--outputs-zip',required=True);p.add_argument('--annotations',required=True);p.add_argument('--out',required=True);p.add_argument('--mode',choices=['confirmatory','exploratory'],default='confirmatory');p.add_argument('--bootstrap',type=int,default=2000);args=p.parse_args()
 out=Path(args.out);out.mkdir(parents=True,exist_ok=True)
 feat,gen,ann,manifest=load(args.outputs_zip,args.annotations);f,a=validate(feat,gen,ann)
 ids=sorted(f,key=int);reviewed=[i for i in ids if a[i]['review_status']=='reviewed' and a[i]['label'] in ('0','1') and a[i]['annotator_id'] and not a[i]['annotator_id'].startswith('AI_')]
 provisional=[i for i in ids if a[i]['label'] in ('0','1')]
 eligible=reviewed if args.mode=='confirmatory' else provisional
 # Never mix pilot with held-out in primary evaluation; common population >=10 tokens for fair method comparison.
 primary=[i for i in eligible if f[i]['partition']=='held_out' and int(f[i]['scored_token_count'])>=10 and all(f[i][k] for k in FEATURES)]
 audit={'mode':args.mode,'input_sha256':{k:hashlib.sha256(Path(v).read_bytes()).hexdigest() for k,v in [('outputs_zip',args.outputs_zip),('annotations',args.annotations)]},'records':len(ids),'pilot':sum(f[i]['partition']=='pilot' for i in ids),'held_out':sum(f[i]['partition']=='held_out' for i in ids),'reviewed_binary':len(reviewed),'provisional_binary':len(provisional),'primary_eligible':len(primary),'primary_correct':sum(a[i]['label']=='0' for i in primary),'primary_incorrect':sum(a[i]['label']=='1' for i in primary),'primary_short_excluded':sum(f[i]['partition']=='held_out' and int(f[i]['scored_token_count'])<10 for i in eligible),'direction':'higher NLL / surprise predicts label 1 (incorrect)','label_warning':'AI-only labels are NOT confirmed ground truth' if args.mode=='exploratory' else None}
 (out/'audit.json').write_text(json.dumps(audit,indent=2))
 rows=[];curves={}
 if len(primary)>1 and len({a[i]['label'] for i in primary})==2:
  y=np.array([int(a[i]['label']) for i in primary]);rng=np.random.default_rng(20261113)
  # paired stratified bootstrap: same sampled IDs across all methods
  pos=np.where(y==1)[0];neg=np.where(y==0)[0]
  boots=[np.concatenate([rng.choice(pos,len(pos),replace=True),rng.choice(neg,len(neg),replace=True)]) for _ in range(args.bootstrap)]
  for k in FEATURES:
   scores=np.array([float(f[i][k]) for i in primary]);auc=roc_auc_score(y,scores);ap=average_precision_score(y,scores)
   ba=np.array([roc_auc_score(y[b],scores[b]) for b in boots]);bp=np.array([average_precision_score(y[b],scores[b]) for b in boots])
   rows.append({'method':k,'n':len(y),'n_incorrect':int(y.sum()),'auroc':auc,'auroc_ci_low':np.quantile(ba,.025),'auroc_ci_high':np.quantile(ba,.975),'auprc':ap,'auprc_ci_low':np.quantile(bp,.025),'auprc_ci_high':np.quantile(bp,.975),'label_status':args.mode})
   curves[k]=(roc_curve(y,scores),precision_recall_curve(y,scores))
  writecsv(out/'results.csv',rows,['method','n','n_incorrect','auroc','auroc_ci_low','auroc_ci_high','auprc','auprc_ci_low','auprc_ci_high','label_status'])
  for kind in ('roc','pr'):
   plt.figure(figsize=(7,5),dpi=160)
   for k,v in curves.items():
    if kind=='roc':(xx,yy,_),_=v
    else:_,(xx,yy,_)=v
    plt.plot(xx,yy,label=k)
   if kind=='roc':plt.plot([0,1],[0,1],'--',color='gray');plt.xlabel('False positive rate');plt.ylabel('True positive rate')
   else:plt.xlabel('Recall');plt.ylabel('Precision')
   plt.title(('ROC' if kind=='roc' else 'Precision–recall')+' — '+args.mode+' labels');plt.legend(fontsize=8);plt.tight_layout();plt.savefig(out/(kind+'.png'));plt.savefig(out/(kind+'.pdf'));plt.close()
  audit['status']='exploratory_only' if args.mode=='exploratory' else 'computed'
 else:
  writecsv(out/'results.csv',[],['method','n','n_incorrect','auroc','auroc_ci_low','auroc_ci_high','auprc','auprc_ci_low','auprc_ci_high','label_status'])
  audit['status']='BLOCKED_INSUFFICIENT_REVIEWED_LABELS_OR_CLASSES'
 (out/'audit.json').write_text(json.dumps(audit,indent=2));print(json.dumps(audit,indent=2))
if __name__=='__main__':main()

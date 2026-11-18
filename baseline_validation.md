# Prompt 10 — Baseline reproduction and validation report

**Audit basis:** Actual `prompt09_outputs(1).zip`, Prompt 09 `runner.py` and `uncertainty.py`, Prompt 07 frozen blueprint, metrics plan and annotation rubric. Audit run locally against saved outputs; **no independent Qwen inference rerun**.

## Verdict
**VERIFIED: file-level baseline integrity and arithmetic.** **UNCERTAIN: independent model reproducibility and comparison to published methods.** **NEEDS CORRECTION before performance claims: factual labels and benchmark-comparable reference evidence.** This is not a published-paper numerical reproduction.

## VERIFIED
- 100 unique sample positions, 20 pilot / 80 held-out; generation and feature CSV records agree on identities and text.
- All 100 outputs contain nonempty scored token sequences; five features recomputed from saved token NLL values exactly match JSONL and CSV (maximum discrepancy 0).
- Model revision pinned `7ae557604adf67be50417f59c2c2f167def9a775`; model `Qwen/Qwen2.5-0.5B-Instruct`; manifest says Tesla T4, float32, greedy, 64-token cap, no cache, seed 20261113.
- 66 EOS completions; 34 capped at 64 tokens. Two answers shorter than 5 scored tokens; 11 shorter than 10; corresponding early-window fields correctly blank.
- Frozen protocol's pilot/held-out split and fixed-window missing-value policy are respected in saved data. No fabricated correctness labels or AUROC/AP.
- Source code implements first-k mean NLL over **nonspecial** generated tokens and full-response mean/max NLL. Higher NLL is the intended higher-risk direction.

## UNCERTAIN — requires more evidence
- Independent rerun agreement: original runtime had a tokenizer `BatchEncoding` compatibility error, patched during execution. The exact patched `runner.py` and Colab cell outputs must be archived to reproduce the executed code, not merely the original source package.
- A second clean-run test on a small frozen subset with the recorded exact package versions is needed. Greedy decoding improves stability but does not guarantee bit-identical outputs across GPU kernels / versions.
- Dataset SHA and sample SHA are recorded in the manifest and validated by Prompt 09 code; verify again against the frozen source files in the final archive and preserve their raw bytes.
- Original published LM-Polygraph / SAR / SelfCheckGPT implementations are **not** implemented as matching numerical baselines here. Full mean NLL and max surprise are operational baselines; claims of paper reproduction require separate matching official code, models, splits, scoring and metrics.
- Raw generation logits are appropriate for model-token surprise, but their interpretation differs from logits modified by generation processors. Record this as a deliberate, justified adaptation, not an exact replication of another pipeline.
- Answers with max-token termination may be incomplete; this affects factual annotation and detector interpretation. Preserve them and flag them, do not silently drop or extend them after seeing labels.

## NEEDS CORRECTION / required next actions
1. Archive the **actual patched** runner source, package versions, restore log and final run logs; confirm the `BatchEncoding` fix did not change the input tokens or scoring.
2. Run `audit_prompt10.py` against the original output ZIP and retain `audit_results.json` and `audit_checks.csv` as independent file-level checks.
3. Produce **blind** correctness labels from the prepared sheet. No uncertainty scores may appear on the annotation sheet. Label 0 correct, 1 incorrect, U unresolved; rationale and evidence source mandatory. Review >=20 examples independently if possible.
4. Verify whether the source TruthfulQA reference fields are sufficient; seek independent factual sources for disputed or ambiguous cases. Never equate benchmark reference-answer text with a correctness label for generated text.
5. Freeze annotations before joining with scores; calculate held-out AUROC/AP only if both classes exist, applying paired `L>=10` population for primary comparisons and documented exclusions.
6. Do not claim exact replication of an external published baseline without a method-to-code audit against its official reference implementation and benchmark protocol.

## Method-to-code audit matrix
| Dimension | Observed implementation | Judgment |
|---|---|---|
| Data | Frozen 790-row TruthfulQA source, 100 sampled questions | VERIFIED for output identities; source hash recheck recommended |
| Split | 20 pilot / 80 held-out | VERIFIED |
| Model | Qwen2.5-0.5B-Instruct pinned revision | VERIFIED in manifest; actual model weights not reloaded here |
| Decoding | Greedy, 64 new tokens, no cache | VERIFIED in source and manifest |
| Seed | 20261113 | VERIFIED in source and manifest; independent rerun pending |
| Scoring | Float32 raw generation logits, nonspecial token NLL | VERIFIED in source and stored features; methodological adaptation |
| Baselines | Full mean NLL and max surprise | VERIFIED operational definitions; not published numerical reproduction |
| Metrics | AUROC/AP, bootstrap CI | NOT RUN: correctness labels unavailable |
| Ground truth | Blind human factual correctness | NEEDS CORRECTION: labels not yet collected |
| Reported-paper numerical comparison | No matched external reference results | UNCERTAIN / NOT CLAIMED |

## Discrepancy register
- Prompt 08 validation originally compared processed generation scores and full forward logits; resolved by comparing raw generation logits and independent per-prefix logits in float32. Keep debugging history.
- Prompt 09 tokenizer return-type mismatch after runtime restart: `BatchEncoding` versus tensor; execution fix needs final source capture.
- 34/100 capped generations and missing fixed windows (2 for first-5; 11 for first-10) are analysis limitations, not failed computations.

**Decision:** Prompt 10 technical audit complete; gate to factual evaluation is **conditional**, pending verified blinded labels and executed-code provenance. Do not compute performance metrics yet.

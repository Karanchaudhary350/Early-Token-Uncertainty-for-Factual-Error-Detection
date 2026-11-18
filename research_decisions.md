# Research Decisions

Collected from existing prompt-stage records; not a complete verbatim chat transcript.


---

## AITR_Prompt_07__research_decisions_prompt07_append.md

# Append to research_decisions.md — Prompt 07

**2026-11-13 — Protocol v1.0 frozen.** Selected a 100-question seeded TruthfulQA generation sample (seed 20261113), with first 20 sampled IDs reserved for pilot/calibration and remaining 80 for held-out evaluation. Model is Qwen/Qwen2.5-0.5B-Instruct, greedy decoding, maximum 64 new tokens, one generation per question. Frozen scores: first-1, first-5, first-10 mean NLL, full mean NLL and full maximum surprise. Primary paired evaluation uses held-out, reliably labeled answers with >=10 scored tokens. Blind factual labels are 0/1/U; unresolved excluded with counts. Primary metric AUROC, secondary AP/AUPRC; paired bootstrap 2,000 replicates with seed 20261113. Length strata <=10 vs >10, pilot-defined 25th percentile for exploratory confident-error analysis. All changes require protocol amendments.

**VERIFIED in planning artifacts:** These choices are specified and frozen; the review supports the motivating research questions.  
**INFERRED:** Study may fit 2–3 days with Colab and a small model.  
**UNKNOWN / pending:** actual dataset revision, GPU access, model execution, token-score validity, annotation reliability, number of eligible labeled examples, and all outcomes.  
**Gate:** conditional GO to Prompt 08, no claim of successful experiments.


---

## AITR_Prompt_08__research_decisions_prompt08_append.md

## Prompt 08 — Environment and smoke-test implementation (2026-11-13)

**Decision:** Provide a Colab notebook and standalone verification script implementing the frozen Prompt 07 smoke-test stage. Preserve exact random sampling, 20/80 partition, greedy decoding and 64-token cap. Use only two predetermined pilot questions for this stage.

**Provenance:** Upstream TruthfulQA generation CSV URL, exact downloaded bytes and SHA256, model revision where accessible, software/hardware versions and raw token scores will be captured by the user's actual Colab run.

**VERIFIED:** Notebook JSON structure validates locally; Python script compiles locally. **NOT VERIFIED:** Successful Colab execution, upstream availability at runtime, exact GPU allocation, actual model outputs and score consistency. **UNKNOWN:** Correctness-label reliability and downstream class balance.

**Gate:** Pending real Colab smoke test. No final experiment or scientific outcome claimed.


---

## AITR_Prompt_09__research_decisions_prompt09_append.md

## Prompt 09 — Implementation decision (2026-11-13)
- Implemented source files for label-free generation and baseline uncertainty extraction.
- Preserved 790-row TruthfulQA source (SHA256 `b8d8ef1e12f98b4f2a9f47abc9765da0640b182b6c5d9b92f0c1a1f2f1e02e5c`) and the frozen 100-question, 20/80 sample from successful Prompt 08 v4.
- Model: `Qwen/Qwen2.5-0.5B-Instruct`, pinned commit `7ae557604adf67be50417f59c2c2f167def9a775`.
- Scoring: float32 raw generation logits, cache disabled, as verified on two Prompt 08 v4 examples; see `protocol_amendment_prompt09.md`.
- Features: first-1/5/10 mean NLL, full-response mean NLL, full-response maximum token surprise.
- Resume: append-only JSONL, one record per completed question, CSV export and manifests; resume by sample_position with input and settings checks.
- Status: source code prepared and unit-tested locally. **Prompt 09 full Colab run pending.** No correctness labels or predictive metrics available.


---

## Prompt_08_FINAL_SAVE__research_decisions_prompt08_FINAL_append.md

## Prompt 08 — Final technical decision (2026-11-13)

Status: **PASS (two-question smoke test)** based on user-provided Colab output `prompt08_outputs(2).zip`. Environment: Tesla T4, float32, Qwen2.5-0.5B-Instruct revision `7ae557604adf67be50417f59c2c2f167def9a775`. TruthfulQA source CSV: 790 rows, SHA256 `b8d8ef1e12f98b4f2a9f47abc9765da0640b182b6c5d9b92f0c1a1f2f1e02e5c`. Frozen sample: 100 (20 pilot, 80 held-out). Raw generation logits versus independent per-prefix forward-pass comparison passed for two responses; max differences 0.0000154376 and 0.0000042915, below 0.02. Do not claim factuality or detection accuracy. Proceed to Prompt 09 only with preserved scoring convention and reproducibility checks.


---

## Prompt_09_FINAL_SAVE__research_decisions_prompt09_FINAL_append.md

# Research decisions log — Prompt 09 final append

- Accepted frozen 100-question baseline run as complete after checking record uniqueness, partition counts, and token-feature arithmetic.
- Retained scoring protocol: float32 raw generation logits, no cache, greedy generation, 64-token maximum.
- Preserved undefined first-5/first-10 windows for answers shorter than those thresholds (2 and 11 responses respectively).
- Flagged 34 max-token-limit responses as potentially truncated; future evaluation must report and consider this limitation.
- No correctness labels, AUROC or AUPRC inferred from uncertainty features.
- Next stage: correctness annotation and evaluation protocol, with pilot/held-out separation preserved.


---

## Prompt_10_BASELINE_AUDIT__research_decisions_prompt10_append.md

# Research decisions — Prompt 10 append

- **Decision:** Accept Prompt 09 generation and feature extraction as file-level VERIFIED (100/100, exact recomputation of five uncertainty features); do not treat it as independent model rerun or reproduction of published numerical findings.
- **Reason:** Operational NLL/max-surprise baselines use a different model and benchmark protocol from many published uncertainty methods. Explicit adaptation required.
- **Risk register:** 34 capped answers, 11 first-10 missing values, 2 first-5 missing values, patched tokenizer BatchEncoding handling, incomplete executed-code provenance.
- **Mitigation:** Archive patched code and versions; blinded correctness annotation; keep U; independent review where possible; apply held-out paired eligibility restrictions before metrics.
- **Gate:** Conditional GO to annotation preparation; NO GO for claims of hallucination detection performance before labels and statistical checks.


---

## Prompt_11_DEBUG_FINAL__research_decisions_prompt11_append.md

# Research decisions log — Prompt 11 append

- **Incident:** Restarted Colab runtime failed at `torch.ones_like(input_ids)` because `input_ids` was `BatchEncoding`.
- **Decision:** Apply minimal type-normalization at the tokenizer output boundary; preserve all frozen experiment settings.
- **Evidence:** User-supplied traceback; later successful 100-record Prompt 09 output; local simulated-interface tests.
- **Uncertainty:** Root cause of session-to-session return-type change not established; do not assert library version drift as fact.
- **Re-run decision:** Do not regenerate already completed answers solely due to this exception; retain final Prompt 09 archive as evidence.
- **Gate:** Debugging incident documented and local fix tests passed; correctness-label review remains pending for evaluation.


---

## Prompt_12_CONTRIBUTION_FINAL__research_decisions_prompt12_append.md

# Append to research_decisions.md — Prompt 12

**2026-11-14 — Contribution pathway selected: B, controlled comparative study.** Frozen comparison is first-1/5/10 mean NLL versus full-response mean NLL, with full maximum surprise as a second baseline, on identical held-out reviewed cases with at least 10 scored tokens. Paired bootstrap: 2,000 replicates, seed 20261113. Length strata <=10 and >10; pilot 25th-percentile threshold for exploratory confidently incorrect failures. No new algorithm claimed, no generation changes, no retrospective hyperparameter tuning.

**Verified:** Prompt 09 file-level audit recorded 100 valid generations; 11 had fewer than 10 scored tokens and 34 reached the generation cap. **Pending:** independent factual review of AI-first-pass annotations, confirmatory metric evaluation, inference about research hypotheses. **Gate:** proceed to Prompt 13 code preparation, not confirmatory interpretation until annotation review.


---

## Prompt_13_EVALUATION__research_decisions_prompt13_append.md

# Research decisions — Prompt 13 (append)

- Evaluated actual Prompt 09 Qwen2.5-0.5B-Instruct generation outputs and first-pass AI annotation, not synthetic metrics.
- Primary comparator population: held-out only, >=10 scored tokens, finite scores for all five features, binary labels. Higher uncertainty predicts incorrectness (positive class 1).
- Preserve strict sample ID, split, question and content matching. Whitespace-only annotation formatting changes are permitted; substantive changes fail alignment.
- Confirmatory gate remains closed: zero human-reviewed labels. No confirmatory AUROC/AUPRC or paper claims.
- Exploratory analysis is explicitly labeled provisional: 61 held-out records, 13 provisional correct, 48 provisional incorrect. Exclude U and short responses; avoid mixing with confirmatory tables.
- Bootstrap: paired, stratified by provisional class, 2000 resamples with seed 20261113; descriptive uncertainty only, not a significance test.
- Required next action: independent, blinded factual verification of labels and pre-specified adjudication before confirmatory re-evaluation.


---

## Prompt_14_INTERPRETATION_FINAL__research_decisions_prompt14_append.md

# Research decisions — Prompt 14 append

- **Date:** 2026-11-14.
- **Decision:** Interpret Prompt 13 exploratory results without claiming confirmation.
- **Evidence:** actual Prompt 09 generation archive and Prompt 13 exploratory metric CSV/audit; 61 held-out common-population examples, 48 provisional positives; 0 independently reviewed binary labels.
- **Result:** AUROC first-1 0.506, first-5 0.397, first-10 0.380, full mean 0.470, full max surprise 0.497. No reliable early-token advantage demonstrated.
- **Interpretation safeguard:** AUPRC values must be compared against 48/61 positive prevalence; one generation run does not support run-to-run claims.
- **Scope limitation:** RQ2 and RQ3 remain unresolved; no observed compute saving, length-stratified effect or confirmed confidently incorrect count.
- **Next gate:** independent blind annotation review before confirmatory analysis or manuscript performance claims.


---

## Prompt_15_MANUSCRIPT__research_decisions_prompt15_append.md

## Prompt 15 — 2026-11-14
- Drafted an IEEE conference-format manuscript from actual frozen protocol and exploratory outputs.
- Kept provisional AI labels separate from independently reviewed ground truth; no confirmatory results claimed.
- Used genuine Prompt 13 ROC and PR figures and its five measured metric rows.
- Restricted citations to four references with metadata present in the supplied literature review; primary-source verification still pending.
- PDF compiled successfully; current draft is 3 pages, below target, pending stronger verified evidence and fuller scholarly treatment.


---

## Prompt_16_PEER_REVIEW__research_decisions_prompt16_append.md

# Research decisions — Prompt 16 append

- **Decision:** Treat Prompt 15 manuscript as a 3-page exploratory draft requiring major revision, not a submission-ready study.
- **Evidence:** Manuscript and Prompt 13 saved metrics agree on five rounded AUROC/AP values; annotation is AI-only and unreviewed.
- **Gate:** Block confirmatory claims pending independent factual-label review, paired re-evaluation, selection/truncation audit.
- **Scope:** Do not claim a novel algorithm, deployed detector, early-stopping savings, equivalence, or numerical reproduction of published methods.
- **Next action:** Address checklist P0, then P1, then P2; preserve existing results and mark any protocol amendment.


# Append to research_decisions.md — Prompt 07

**2026-11-13 — Protocol v1.0 frozen.** Selected a 100-question seeded TruthfulQA generation sample (seed 20261113), with first 20 sampled IDs reserved for pilot/calibration and remaining 80 for held-out evaluation. Model is Qwen/Qwen2.5-0.5B-Instruct, greedy decoding, maximum 64 new tokens, one generation per question. Frozen scores: first-1, first-5, first-10 mean NLL, full mean NLL and full maximum surprise. Primary paired evaluation uses held-out, reliably labeled answers with >=10 scored tokens. Blind factual labels are 0/1/U; unresolved excluded with counts. Primary metric AUROC, secondary AP/AUPRC; paired bootstrap 2,000 replicates with seed 20261113. Length strata <=10 vs >10, pilot-defined 25th percentile for exploratory confident-error analysis. All changes require protocol amendments.

**VERIFIED in planning artifacts:** These choices are specified and frozen; the review supports the motivating research questions.  
**INFERRED:** Study may fit 2–3 days with Colab and a small model.  
**UNKNOWN / pending:** actual dataset revision, GPU access, model execution, token-score validity, annotation reliability, number of eligible labeled examples, and all outcomes.  
**Gate:** conditional GO to Prompt 08, no claim of successful experiments.

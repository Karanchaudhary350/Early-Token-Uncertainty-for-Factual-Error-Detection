# Research decisions — Prompt 13 (append)

- Evaluated actual Prompt 09 Qwen2.5-0.5B-Instruct generation outputs and first-pass AI annotation, not synthetic metrics.
- Primary comparator population: held-out only, >=10 scored tokens, finite scores for all five features, binary labels. Higher uncertainty predicts incorrectness (positive class 1).
- Preserve strict sample ID, split, question and content matching. Whitespace-only annotation formatting changes are permitted; substantive changes fail alignment.
- Confirmatory gate remains closed: zero human-reviewed labels. No confirmatory AUROC/AUPRC or paper claims.
- Exploratory analysis is explicitly labeled provisional: 61 held-out records, 13 provisional correct, 48 provisional incorrect. Exclude U and short responses; avoid mixing with confirmatory tables.
- Bootstrap: paired, stratified by provisional class, 2000 resamples with seed 20261113; descriptive uncertainty only, not a significance test.
- Required next action: independent, blinded factual verification of labels and pre-specified adjudication before confirmatory re-evaluation.

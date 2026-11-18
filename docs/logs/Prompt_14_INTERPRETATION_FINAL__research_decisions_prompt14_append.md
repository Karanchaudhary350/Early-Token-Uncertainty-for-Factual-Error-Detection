# Research decisions — Prompt 14 append

- **Date:** 2026-11-14.
- **Decision:** Interpret Prompt 13 exploratory results without claiming confirmation.
- **Evidence:** actual Prompt 09 generation archive and Prompt 13 exploratory metric CSV/audit; 61 held-out common-population examples, 48 provisional positives; 0 independently reviewed binary labels.
- **Result:** AUROC first-1 0.506, first-5 0.397, first-10 0.380, full mean 0.470, full max surprise 0.497. No reliable early-token advantage demonstrated.
- **Interpretation safeguard:** AUPRC values must be compared against 48/61 positive prevalence; one generation run does not support run-to-run claims.
- **Scope limitation:** RQ2 and RQ3 remain unresolved; no observed compute saving, length-stratified effect or confirmed confidently incorrect count.
- **Next gate:** independent blind annotation review before confirmatory analysis or manuscript performance claims.

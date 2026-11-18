# Limitations and scope

- Single small language model, single frozen 100-question sample and one decoding run.
- 20 pilot / 80 held-out; the common-population exploratory comparison has 61 held-out answers, of which 48 are provisionally incorrect.
- Eleven responses across all 100 had fewer than 10 scored tokens; short-window features are missing by design. Unresolved labels and eligibility exclusions also reduce sample size.
- Thirty-four outputs reached the 64-token cap, so some answers may be incomplete.
- No independent correctness verification; provisional AI labels may be biased or wrong.
- Exploratory AUROC is near chance; high AUPRC is influenced by the ~79% positive-class prevalence.
- Paired bootstrap CIs are descriptive conditional on the sample and provisional labels; no independent model rerun.
- RQ2 answer length and RQ3 confidently incorrect answers remain unresolved.
- Paper is a draft; peer review recommends major revision. No verified claim of publication or acceptance.

# Prioritized manuscript revision checklist

## P0 — Evidence blockers (must address before confirmatory findings)
- [ ] Independently review the AI-first-pass factual labels; record reviewer IDs, evidence, disagreements and adjudication.
- [ ] Re-run the held-out comparison only on the prespecified reviewed-label population; publish class counts and exclusions.
- [ ] Report paired bootstrap differences of each early-window AUROC versus full-response AUROC; no unsupported significance/equivalence language.

## P1 — Design and reproducibility
- [ ] Report exactly why 19/80 held-out records are absent from the common-population analysis; assess selection sensitivity.
- [ ] Audit the 64-token cap within the analysis population and response-completeness effects.
- [ ] Execute RQ2 length strata and RQ3 pilot-frozen confidence-failure protocol, or formally narrow the paper scope.
- [ ] Include exact model/dataset revisions, SHA256, environment, generation template, patched runner and executed commands.
- [ ] Clarify that semantic entropy/SelfCheckGPT were related-work comparators, not executed baselines.

## P2 — Manuscript quality
- [ ] Verify bibliography from primary records and resolve `.bib` vs embedded references.
- [ ] Expand the manuscript from 3 to the assignment’s 6–10 pages using genuine methods/results and limitations.
- [ ] Add token/EOS handling, smoke-test tolerance and diagnostics.
- [ ] Improve ROC/PR captions and inspect the compiled PDF at print size.
- [ ] Fill author/affiliation only with verified information.

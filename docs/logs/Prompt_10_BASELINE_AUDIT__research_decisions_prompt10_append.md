# Research decisions — Prompt 10 append

- **Decision:** Accept Prompt 09 generation and feature extraction as file-level VERIFIED (100/100, exact recomputation of five uncertainty features); do not treat it as independent model rerun or reproduction of published numerical findings.
- **Reason:** Operational NLL/max-surprise baselines use a different model and benchmark protocol from many published uncertainty methods. Explicit adaptation required.
- **Risk register:** 34 capped answers, 11 first-10 missing values, 2 first-5 missing values, patched tokenizer BatchEncoding handling, incomplete executed-code provenance.
- **Mitigation:** Archive patched code and versions; blinded correctness annotation; keep U; independent review where possible; apply held-out paired eligibility restrictions before metrics.
- **Gate:** Conditional GO to annotation preparation; NO GO for claims of hallucination detection performance before labels and statistical checks.

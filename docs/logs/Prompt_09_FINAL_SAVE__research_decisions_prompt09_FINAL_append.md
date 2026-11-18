# Research decisions log — Prompt 09 final append

- Accepted frozen 100-question baseline run as complete after checking record uniqueness, partition counts, and token-feature arithmetic.
- Retained scoring protocol: float32 raw generation logits, no cache, greedy generation, 64-token maximum.
- Preserved undefined first-5/first-10 windows for answers shorter than those thresholds (2 and 11 responses respectively).
- Flagged 34 max-token-limit responses as potentially truncated; future evaluation must report and consider this limitation.
- No correctness labels, AUROC or AUPRC inferred from uncertainty features.
- Next stage: correctness annotation and evaluation protocol, with pilot/held-out separation preserved.

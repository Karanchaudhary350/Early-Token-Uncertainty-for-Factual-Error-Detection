# Research decisions log — Prompt 11 append

- **Incident:** Restarted Colab runtime failed at `torch.ones_like(input_ids)` because `input_ids` was `BatchEncoding`.
- **Decision:** Apply minimal type-normalization at the tokenizer output boundary; preserve all frozen experiment settings.
- **Evidence:** User-supplied traceback; later successful 100-record Prompt 09 output; local simulated-interface tests.
- **Uncertainty:** Root cause of session-to-session return-type change not established; do not assert library version drift as fact.
- **Re-run decision:** Do not regenerate already completed answers solely due to this exception; retain final Prompt 09 archive as evidence.
- **Gate:** Debugging incident documented and local fix tests passed; correctness-label review remains pending for evaluation.

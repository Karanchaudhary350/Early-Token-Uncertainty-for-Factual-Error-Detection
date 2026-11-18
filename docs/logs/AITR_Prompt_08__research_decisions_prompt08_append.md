## Prompt 08 — Environment and smoke-test implementation (2026-11-13)

**Decision:** Provide a Colab notebook and standalone verification script implementing the frozen Prompt 07 smoke-test stage. Preserve exact random sampling, 20/80 partition, greedy decoding and 64-token cap. Use only two predetermined pilot questions for this stage.

**Provenance:** Upstream TruthfulQA generation CSV URL, exact downloaded bytes and SHA256, model revision where accessible, software/hardware versions and raw token scores will be captured by the user's actual Colab run.

**VERIFIED:** Notebook JSON structure validates locally; Python script compiles locally. **NOT VERIFIED:** Successful Colab execution, upstream availability at runtime, exact GPU allocation, actual model outputs and score consistency. **UNKNOWN:** Correctness-label reliability and downstream class balance.

**Gate:** Pending real Colab smoke test. No final experiment or scientific outcome claimed.

## Prompt 09 — Implementation decision (2026-11-13)
- Implemented source files for label-free generation and baseline uncertainty extraction.
- Preserved 790-row TruthfulQA source (SHA256 `b8d8ef1e12f98b4f2a9f47abc9765da0640b182b6c5d9b92f0c1a1f2f1e02e5c`) and the frozen 100-question, 20/80 sample from successful Prompt 08 v4.
- Model: `Qwen/Qwen2.5-0.5B-Instruct`, pinned commit `7ae557604adf67be50417f59c2c2f167def9a775`.
- Scoring: float32 raw generation logits, cache disabled, as verified on two Prompt 08 v4 examples; see `protocol_amendment_prompt09.md`.
- Features: first-1/5/10 mean NLL, full-response mean NLL, full-response maximum token surprise.
- Resume: append-only JSONL, one record per completed question, CSV export and manifests; resume by sample_position with input and settings checks.
- Status: source code prepared and unit-tested locally. **Prompt 09 full Colab run pending.** No correctness labels or predictive metrics available.

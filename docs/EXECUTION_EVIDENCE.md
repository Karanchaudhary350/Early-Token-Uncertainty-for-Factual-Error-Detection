# Execution evidence: what was and was not run

**Previously executed (supported by archived outputs and stage reports):**
- Prompt 08 raw-logit validation, two examples; the stage report records small logit differences.
- Prompt 09 user Colab generation produced 100 JSONL records and 100 feature rows; file-level validation was reported as passing. This is not an independent model rerun.
- Prompt 11 four local compatibility tests were reported passing; test transcript and patch are from that stage, not a new clean-room run.
- Prompt 13 exploratory evaluation produced the included metrics and figures from provisional AI labels; confirmatory metrics remain empty.
- Prompt 15 manuscript PDF was compiled previously; not recompiled for this repository.

**Not yet verified:**
- Fresh model generation in this repository and clean-room execution on another system.
- Fresh environment install across all platforms; GPU/CUDA availability.
- Independent factual verification, confirmatory metrics, RQ2/RQ3 analyses.
- Publication permissions for bundled dataset, model outputs, and manuscript references.

**Prompt 17 local checks** are recorded in `docs/PROMPT17_CHECKS.json`; they are static/file integrity and lightweight Python checks, not a model rerun.

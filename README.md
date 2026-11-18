# Early-Token Uncertainty for Factual Error Detection

**Reproducibility archive — exploratory results only; NOT independently verified ground truth.**

A controlled comparison of first-1, first-5, first-10 and full-response mean negative log-likelihood (NLL), plus full-response maximum token surprise, for factual-error detection using Qwen/Qwen2.5-0.5B-Instruct on a frozen 100-question TruthfulQA sample.

## Status and key results

- Frozen sample: 20 pilot and 80 held-out questions; 100 actual generated responses saved.
- Evaluation: 61 common-population held-out responses with provisional binary labels (48 incorrect, 13 correct). The five AUROCs were approximately 0.506, 0.397, 0.380, 0.470 and 0.497, respectively.
- **Confirmatory evaluation blocked**: no independently reviewed correctness labels. RQ2/RQ3 remain unresolved. See `docs/LIMITATIONS.md`.

## Layout

- `src/runner.py`, `src/uncertainty.py`: actual Prompt 09 generator/feature code, with the documented Prompt 11 BatchEncoding patch applied.
- `src/evaluate.py`: Prompt 13 evaluation script.
- `notebooks/`: original Colab notebook.
- `data/frozen/`: exact frozen source CSV and sample (check redistribution permissions).
- `data/outputs/`: original 100-response run, metadata and evaluation input ZIP.
- `data/annotations/`: **unreviewed AI-first-pass** labels, not ground truth.
- `results/`: saved exploratory metrics and figures; empty confirmatory metrics.
- `paper/`: latest results-focused Springer LNCS manuscript, figures, and bibliography (verify references before submission).
- `docs/`: methodology caveats, review, provenance, execution evidence, credits, logs and checklist.

## Setup

Generation (GPU recommended; **[TEST REQUIRED]** on a fresh environment):

```bash
python -m pip install -r configs/requirements-generation.txt
```

Evaluation only (**[TEST REQUIRED]** in a fresh environment):

```bash
python -m pip install -r configs/requirements-evaluation.txt
bash scripts/reproduce_evaluation.sh
```

Check dataset/sample hashes (no external dependencies):

```bash
python scripts/verify_inputs.py
```

For the original Colab workflow, inspect `notebooks/Prompt_09_Baseline_Colab.ipynb` and `src/runner.py`; the original notebook may refer to the earlier `modules/` layout. **[TEST REQUIRED]**: adapt notebook imports to the repository structure and perform a new end-to-end generation run. Do not assume the notebook executes unchanged.

## Integrity and responsible use

Read `docs/EXECUTION_EVIDENCE.md` to distinguish previously executed experiments from untested commands. See `docs/DATA_ACCESS.md` for provenance, hashes and distribution checks; `docs/REPRODUCTION_CHECKLIST.md` for open tasks; `docs/CREDITS_AND_DISCLOSURES.md` for attribution and AI use.

**Before making this repository public:** verify TruthfulQA redistribution rights, confirm the license owner, audit sensitive information, and independently review correctness labels. This package is organized for public release but is **not certified publication-ready**.

## Assignment-required files

The root matches the **suggested project tree** in Section 9 of `AI_Tools_for_Research_post_mid_sem_assignment.pdf`: `README.md`, `requirements.txt`, `configs/`, `data/README.md`, `notebooks/`, `src/`, `scripts/`, `results/`, `paper/`, `research_decisions.md`, `baseline_validation.md`, `ai_assistance_log.md`. Supporting documentation is in `docs/` and tests in `tests/`.

**Latest paper:** `paper/main.tex` (Springer LNCS results-focused revision), `paper/main.pdf`; required figure assets are in `paper/figures/`. Paired AUROC differences, answer-length and confidence audits are in `results/exploratory/`. These are calculations on provisional labels.

**Publication gate:** `LICENSE_REVIEW_REQUIRED.txt` contains a prior draft license whose ownership has not been confirmed; choose an authorized license before publication. Dataset redistribution and citation verification are also outstanding.

**Do not publish blindly:** inspect `data/` and metadata for permissions/private data. Re-run and independently validate the experiment before claiming reproducibility on another machine.
# Early-Token-Uncertainty-for-Factual-Error-Detection

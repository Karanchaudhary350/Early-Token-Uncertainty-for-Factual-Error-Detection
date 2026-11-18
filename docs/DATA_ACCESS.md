# Data access and provenance

The repository includes the exact local TruthfulQA source CSV and frozen sample CSV used by the original runner. **Before public release**, check the dataset license, attribution, and whether redistributing the bundled source CSV is permitted; if not, remove it and document the official acquisition route and SHA256. The frozen source is 790 rows; the sample is 100 questions (20 pilot, 80 held-out).

`data/outputs/` contains actual user-supplied Colab outputs (100 responses), plus the original ZIP consumed by the evaluation script. `data/annotations/AI_first_pass_UNVERIFIED.csv` is **AI-provisional**, not independently reviewed ground truth. Do not present the exploratory results as confirmatory.

No model weights are bundled. The runner requests `Qwen/Qwen2.5-0.5B-Instruct` at the frozen revision recorded in the manifest. Consult the model card and license before redistributing weights or derived artifacts.

To verify the frozen dataset and sample, run `python scripts/verify_inputs.py`. The script checks hashes against the actual runner constants; it does not download or authenticate the upstream dataset.

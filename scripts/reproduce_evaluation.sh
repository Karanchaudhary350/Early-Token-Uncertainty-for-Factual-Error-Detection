#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
python src/evaluate.py --outputs-zip data/outputs/prompt09_outputs_original.zip --annotations data/annotations/AI_first_pass_UNVERIFIED.csv --out outputs_new/confirmatory
python src/evaluate.py --outputs-zip data/outputs/prompt09_outputs_original.zip --annotations data/annotations/AI_first_pass_UNVERIFIED.csv --out outputs_new/exploratory --mode exploratory

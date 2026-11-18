from pathlib import Path
import hashlib,sys
root=Path(__file__).resolve().parents[1]
expected={'data/frozen/TruthfulQA_source.csv':'b8d8ef1e12f98b4f2a9f47abc9765da0640b182b6c5d9b92f0c1a1f2f1e02e5c','data/frozen/frozen_sample_ids.csv':'88b8993dfa8535f8e0c8fc6055d511243405ee3605e9fb3fc53d6b1f5da0b589'}
failed=False
for name,want in expected.items():
 p=root/name;got=hashlib.sha256(p.read_bytes()).hexdigest();ok=got==want
 print(('PASS' if ok else 'FAIL'),name,got);failed |= not ok
sys.exit(1 if failed else 0)

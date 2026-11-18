"""Prompt 11: minimal tokenizer-return compatibility patch.

Apply to original Prompt 09 runner.py. This script does not run the model.
"""
from pathlib import Path
import sys

OLD = "input_ids = tokenizer.apply_chat_template(messages, tokenize=True, add_generation_prompt=True, return_tensors='pt').to(device)"
NEW = """encoded = tokenizer.apply_chat_template(messages, tokenize=True, add_generation_prompt=True, return_tensors='pt')
    input_ids = (encoded['input_ids'] if hasattr(encoded, 'keys') else encoded).to(device)"""

def patch(path):
    p = Path(path)
    src = p.read_text()
    if NEW in src:
        return 'already patched'
    if src.count(OLD) != 1:
        raise RuntimeError('Expected exactly one matching statement; refusing to modify file')
    backup = p.with_suffix(p.suffix + '.before_prompt11')
    if not backup.exists():
        backup.write_text(src)
    p.write_text(src.replace(OLD, NEW, 1))
    compile(p.read_text(), str(p), 'exec')
    return 'patched; backup: ' + str(backup)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit('Usage: python runner_patch.py /path/to/runner.py')
    print(patch(sys.argv[1]))

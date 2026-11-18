"""Lightweight unit checks; no model weights or Colab GPU needed."""
import tempfile
from pathlib import Path
from runner_patch import OLD, NEW, patch

class DummyTensor:
    def to(self, device):
        self.device = device
        return self

class DummyBatchEncoding(dict):
    def to(self, device):
        for value in self.values():
            value.to(device)
        return self

def extract(value, device):
    return (value['input_ids'] if hasattr(value, 'keys') else value).to(device)

def test_tensor_case():
    t = DummyTensor()
    assert extract(t, 'cpu') is t
    assert t.device == 'cpu'

def test_batch_encoding_case():
    t = DummyTensor()
    assert extract(DummyBatchEncoding(input_ids=t), 'cpu') is t

def test_patch_idempotent_and_syntax():
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / 'runner.py'
        p.write_text('def f(tokenizer, messages, device):\n    ' + OLD + '\n    return input_ids\n')
        assert patch(p).startswith('patched;')
        assert NEW in p.read_text()
        assert patch(p) == 'already patched'
        assert p.with_suffix('.py.before_prompt11').exists()

def test_refuses_unexpected_source():
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / 'runner.py'
        p.write_text('def f(): pass\n')
        try:
            patch(p)
        except RuntimeError:
            return
        raise AssertionError('Expected refusal')

if __name__ == '__main__':
    for fn in (test_tensor_case, test_batch_encoding_case, test_patch_idempotent_and_syntax, test_refuses_unexpected_source):
        fn()
        print('PASS', fn.__name__)

"""Frozen, label-free uncertainty feature extraction. Higher NLL means higher risk."""
import math

FEATURES = ('first_1_mean_nll','first_5_mean_nll','first_10_mean_nll','full_mean_nll','full_max_surprise')

def compute_features(nll):
    values = [float(v) for v in nll]
    if any(not math.isfinite(v) or v < -1e-5 for v in values):
        raise ValueError('Nonfinite or negative token surprise')
    n = len(values)
    return {
        'first_1_mean_nll': values[0] if n >= 1 else None,
        'first_5_mean_nll': sum(values[:5])/5 if n >= 5 else None,
        'first_10_mean_nll': sum(values[:10])/10 if n >= 10 else None,
        'full_mean_nll': sum(values)/n if n else None,
        'full_max_surprise': max(values) if n else None,
    }

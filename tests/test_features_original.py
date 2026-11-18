import unittest
from uncertainty import compute_features

class FeatureTests(unittest.TestCase):
    def test_empty(self):
        self.assertTrue(all(v is None for v in compute_features([]).values()))
    def test_short(self):
        x = compute_features([1,2,3])
        self.assertEqual(x['first_1_mean_nll'],1)
        self.assertIsNone(x['first_5_mean_nll'])
        self.assertEqual(x['full_mean_nll'],2)
        self.assertEqual(x['full_max_surprise'],3)
    def test_long(self):
        x=compute_features(list(range(1,12)))
        self.assertEqual(x['first_5_mean_nll'],3)
        self.assertEqual(x['first_10_mean_nll'],5.5)
        self.assertEqual(x['full_mean_nll'],6)
if __name__=='__main__': unittest.main()

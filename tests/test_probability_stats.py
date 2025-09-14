import unittest
from priyam.probability_stats import mean, median, mode, variance, standard_deviation, permutations, combinations, binomial_probability, linear_regression

class TestProbabilityStats(unittest.TestCase):
    
    def test_mean(self):
        self.assertEqual(mean([1, 2, 3, 4, 5]), 3.0)
        self.assertEqual(mean([10]), 10.0)
    
    def test_median(self):
        self.assertEqual(median([1, 2, 3, 4, 5]), 3.0)
        self.assertEqual(median([1, 2, 3, 4]), 2.5)
    
    def test_mode(self):
        self.assertEqual(mode([1, 2, 2, 3, 4]), [2])
        self.assertEqual(mode([1, 1, 2, 2, 3]), [1, 2])
    
    def test_variance(self):
        data = [1, 2, 3, 4, 5]
        self.assertAlmostEqual(variance(data), 2.5)
        self.assertAlmostEqual(variance(data, sample=False), 2.0)
    
    def test_permutations_combinations(self):
        self.assertEqual(permutations(5, 2), 20)
        self.assertEqual(combinations(5, 2), 10)
        self.assertEqual(combinations(5, 0), 1)
    
    def test_binomial_probability(self):
        self.assertAlmostEqual(binomial_probability(5, 2, 0.5), 0.3125)
        self.assertAlmostEqual(binomial_probability(3, 3, 0.5), 0.125)
    
    def test_linear_regression(self):
        x = [1, 2, 3, 4, 5]
        y = [2, 4, 5, 4, 5]
        slope, intercept = linear_regression(x, y)
        self.assertAlmostEqual(slope, 0.6)
        self.assertAlmostEqual(intercept, 2.2)

if __name__ == "__main__":
    unittest.main()
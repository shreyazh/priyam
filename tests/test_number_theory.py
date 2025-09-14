import unittest
from priyam.number_theory import generate_primes, prime_factorization, is_perfect_number, simplify_fraction, modular_inverse

class TestNumberTheory(unittest.TestCase):
    
    def test_generate_primes(self):
        self.assertEqual(generate_primes(5), [2, 3, 5, 7, 11])
        self.assertEqual(generate_primes(1), [2])
        self.assertEqual(generate_primes(0), [])
    
    def test_prime_factorization(self):
        self.assertEqual(prime_factorization(60), {2: 2, 3: 1, 5: 1})
        self.assertEqual(prime_factorization(17), {17: 1})
        self.assertEqual(prime_factorization(1), {})
    
    def test_is_perfect_number(self):
        self.assertTrue(is_perfect_number(6))
        self.assertTrue(is_perfect_number(28))
        self.assertFalse(is_perfect_number(10))
        self.assertFalse(is_perfect_number(1))
    
    def test_simplify_fraction(self):
        self.assertEqual(simplify_fraction(8, 12), (2, 3))
        self.assertEqual(simplify_fraction(5, 7), (5, 7))
        with self.assertRaises(ValueError):
            simplify_fraction(5, 0)
    
    def test_modular_inverse(self):
        self.assertEqual(modular_inverse(3, 11), 4)
        self.assertEqual(modular_inverse(2, 5), 3)

if __name__ == "__main__":
    unittest.main()
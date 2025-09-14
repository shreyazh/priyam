import unittest
import math
from priyam.algebra import solve_linear, solve_quadratic, solve_cubic, matrix_determinant

class TestAlgebra(unittest.TestCase):
    
    def test_solve_linear(self):
        self.assertEqual(solve_linear(2, -4), 2.0)
        self.assertEqual(solve_linear(0, 0), "Infinite solutions")
        self.assertEqual(solve_linear(0, 5), "No solution")
    
    def test_solve_quadratic(self):
        # Two real roots
        roots = solve_quadratic(1, -3, 2)
        self.assertAlmostEqual(roots[0], 2.0)
        self.assertAlmostEqual(roots[1], 1.0)
        
        # One real root
        roots = solve_quadratic(1, -2, 1)
        self.assertAlmostEqual(roots[0], 1.0)
        self.assertAlmostEqual(roots[1], 1.0)
    
    def test_matrix_determinant(self):
        self.assertEqual(matrix_determinant([[1, 2], [3, 4]]), -2)
        self.assertEqual(matrix_determinant([[5]]), 5)
        self.assertEqual(matrix_determinant([[2, 3, 1], [1, 2, 3], [3, 1, 2]]), -18)

if __name__ == "__main__":
    unittest.main()
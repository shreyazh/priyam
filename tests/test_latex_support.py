import unittest
from priyam.latex_support import latex_fraction, latex_equation, latex_matrix

class TestLatexSupport(unittest.TestCase):
    
    def test_latex_fraction(self):
        self.assertEqual(latex_fraction(1, 2), "\\frac{1}{2}")
        self.assertEqual(latex_fraction("a", "b"), "\\frac{a}{b}")
        self.assertEqual(latex_fraction("x^2", "y^3"), "\\frac{x^2}{y^3}")
    
    def test_latex_equation(self):
        self.assertEqual(latex_equation("ax^2 + bx + c = 0"), "ax^2 + bx + c = 0")
        self.assertEqual(latex_equation("E = mc^2"), "E = mc^2")
        self.assertEqual(latex_equation("y = mx + b", "x"), "y = mx + b")
    
    def test_latex_matrix(self):
        matrix = [[1, 2], [3, 4]]
        self.assertEqual(latex_matrix(matrix), "\\begin{bmatrix} 1 & 2 \\\\ 3 & 4 \\end{bmatrix}")
        
        matrix_3x3 = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        expected = "\\begin{bmatrix} 1 & 2 & 3 \\\\ 4 & 5 & 6 \\\\ 7 & 8 & 9 \\end{bmatrix}"
        self.assertEqual(latex_matrix(matrix_3x3), expected)

if __name__ == "__main__":
    unittest.main()
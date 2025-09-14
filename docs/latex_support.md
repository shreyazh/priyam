# LaTeX Support Utilities

Functions for generating LaTeX code for mathematical expressions. These utilities help create properly formatted mathematical expressions for documentation, reports, and educational materials.

## Functions

### `latex_fraction(numerator, denominator)`

Generate LaTeX code for a fraction.

**Parameters:**
- `numerator` (str or numeric): The numerator of the fraction.
- `denominator` (str or numeric): The denominator of the fraction.

**Returns:**
- str: LaTeX code for the fraction.

**Example:**
```python
from priyam.latex_support import latex_fraction

# Basic fraction
print(latex_fraction(1, 2))  # \frac{1}{2}

# Fraction with variables
print(latex_fraction("x^2", "y^3"))  # \frac{x^2}{y^3}

# Complex expressions
print(latex_fraction("a + b", "c - d"))  # \frac{a + b}{c - d}

----
from priyam.latex_support import latex_equation

# Quadratic equation
print(latex_equation("ax^2 + bx + c = 0"))  # ax^2 + bx + c = 0

# Einstein's equation
print(latex_equation("E = mc^2"))  # E = mc^2

# Linear equation
print(latex_equation("y = mx + b", "x"))  # y = mx + b
---
from priyam.latex_support import latex_matrix

# 2x2 matrix
matrix = [[1, 2], [3, 4]]
print(latex_matrix(matrix))  # \begin{bmatrix} 1 & 2 \\ 3 & 4 \end{bmatrix}

# 3x3 matrix
matrix_3x3 = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
result = latex_matrix(matrix_3x3)
print(result)  # \begin{bmatrix} 1 & 2 & 3 \\ 4 & 5 & 6 \\ 7 & 8 & 9 \end{bmatrix}

# Matrix with variables
var_matrix = [["a", "b"], ["c", "d"]]
print(latex_matrix(var_matrix))  # \begin{bmatrix} a & b \\ c & d \end{bmatrix}
---
from priyam.latex_support import latex_fraction, latex_equation, latex_matrix

# Create a LaTeX document with various mathematical elements
latex_content = f"""
\\documentclass{{article}}
\\usepackage{{amsmath}}
\\begin{{document}}

\\section{{Mathematical Expressions}}

A fraction: ${latex_fraction(1, 2)}$

An equation: ${latex_equation("x^2 + y^2 = z^2")}$

A matrix:
\\[
{latex_matrix([[1, 2], [3, 4]])}
\\]

\\end{{document}}
"""

print(latex_content)
---
from priyam.latex_support import latex_fraction

def create_math_problem(numerator, denominator):
    """Create a fraction simplification problem with LaTeX formatting."""
    fraction = latex_fraction(numerator, denominator)
    return f"Simplify the fraction: ${fraction}$"

problem = create_math_problem(8, 12)
print(problem)  # Simplify the fraction: $\frac{8}{12}$
---

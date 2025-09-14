
### docs/algebra.md
```markdown
# Algebra Utilities

Functions for algebraic operations and equation solving.

## Functions

### `solve_linear(a, b)`

Solve a linear equation of the form ax + b = 0.

**Parameters:**
- `a` (float): Coefficient of x.
- `b` (float): Constant term.

**Returns:**
- float or str: The solution to the equation.

**Example:**
```python
from priyam.algebra import solve_linear

print(solve_linear(2, -4))  # 2.0
---
\[
ax^2 + bx + c = 0
\]

### Parameters
- **a** (*float*): Coefficient of \(x^2\).  
- **b** (*float*): Coefficient of \(x\).  
- **c** (*float*): Constant term.  

### Returns
- **tuple**: The solutions to the equation.

### Example
```python
from priyam.algebra import solve_quadratic

print(solve_quadratic(1, -3, 2))  # (2.0, 1.0)
---
from priyam.algebra import solve_cubic

print(solve_cubic(1, -6, 11, -6))  # (3.0, 2.0, 1.0)
---
from priyam.algebra import matrix_determinant

matrix = [[1, 2], [3, 4]]
print(matrix_determinant(matrix))  # -2.0

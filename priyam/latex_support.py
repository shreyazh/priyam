"""
LaTeX support for pretty printing equations.
"""

def latex_fraction(numerator, denominator):
    """
    Generate LaTeX code for a fraction.
    
    Args:
        numerator: The numerator of the fraction.
        denominator: The denominator of the fraction.
        
    Returns:
        str: LaTeX code for the fraction.
        
    Example:
        >>> latex_fraction(1, 2)
        '\\frac{1}{2}'
    """
    return f"\\frac{{{numerator}}}{{{denominator}}}"

def latex_equation(expression, variable="x"):
    """
    Generate LaTeX code for an equation.
    
    Args:
        expression: The expression to format.
        variable: The variable in the equation.
        
    Returns:
        str: LaTeX code for the equation.
        
    Example:
        >>> latex_equation("ax^2 + bx + c = 0")
        'ax^2 + bx + c = 0'
    """
    # This is a simplified version - in a real implementation,
    # you would parse the expression and convert it to LaTeX
    return expression

def latex_matrix(matrix):
    """
    Generate LaTeX code for a matrix.
    
    Args:
        matrix: The matrix to format.
        
    Returns:
        str: LaTeX code for the matrix.
        
    Example:
        >>> latex_matrix([[1, 2], [3, 4]])
        '\\begin{bmatrix} 1 & 2 \\\\ 3 & 4 \\end{bmatrix}'
    """
    rows = [" & ".join(map(str, row)) for row in matrix]
    matrix_body = " \\\\ ".join(rows)
    return f"\\begin{{bmatrix}} {matrix_body} \\end{{bmatrix}}"
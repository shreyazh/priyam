"""
Algebra utilities for equation solving and symbolic operations.
"""

import cmath
import math
import re
from collections import defaultdict

def solve_linear(a, b):
    """
    Solve a linear equation of the form ax + b = 0.
    
    Args:
        a (float): Coefficient of x.
        b (float): Constant term.
        
    Returns:
        float: The solution to the equation.
        
    Example:
        >>> solve_linear(2, -4)
        2.0
    """
    if a == 0:
        if b == 0:
            return "Infinite solutions"
        else:
            return "No solution"
    return -b / a

def solve_quadratic(a, b, c):
    """
    Solve a quadratic equation of the form ax² + bx + c = 0.
    
    Args:
        a (float): Coefficient of x².
        b (float): Coefficient of x.
        c (float): Constant term.
        
    Returns:
        tuple: The solutions to the equation.
        
    Example:
        >>> solve_quadratic(1, -3, 2)
        (2.0, 1.0)
    """
    if a == 0:
        return solve_linear(b, c)
    
    discriminant = b**2 - 4*a*c
    
    if discriminant > 0:
        root1 = (-b + math.sqrt(discriminant)) / (2*a)
        root2 = (-b - math.sqrt(discriminant)) / (2*a)
        return root1, root2
    elif discriminant == 0:
        root = -b / (2*a)
        return root, root
    else:
        root1 = (-b + cmath.sqrt(discriminant)) / (2*a)
        root2 = (-b - cmath.sqrt(discriminant)) / (2*a)
        return root1, root2

def solve_cubic(a, b, c, d):
    """
    Solve a cubic equation of the form ax³ + bx² + cx + d = 0.
    
    Args:
        a (float): Coefficient of x³.
        b (float): Coefficient of x².
        c (float): Coefficient of x.
        d (float): Constant term.
        
    Returns:
        tuple: The solutions to the equation.
        
    Example:
        >>> solve_cubic(1, -6, 11, -6)
        (3.0, 2.0, 1.0)
    """
    if a == 0:
        return solve_quadratic(b, c, d)
    
    # Normalize the equation: x³ + px² + qx + r = 0
    p = b / a
    q = c / a
    r = d / a
    
    # Depressed cubic: y³ + my + n = 0 where y = x + p/3
    p3 = p / 3
    m = q - p * p3
    n = 2 * p3**3 - p3 * q + r
    
    # Cardano's formula
    discriminant = (n/2)**2 + (m/3)**3
    
    if discriminant > 0:
        u = (-n/2 + math.sqrt(discriminant))**(1/3)
        v = (-n/2 - math.sqrt(discriminant))**(1/3)
        y1 = u + v
        roots = [y1 - p3]
    elif discriminant == 0:
        u = (-n/2)**(1/3)
        y1 = 2 * u
        y2 = -u
        roots = [y1 - p3, y2 - p3, y2 - p3]
    else:
        rho = math.sqrt((-m/3)**3)
        theta = math.acos(-n/(2*rho))
        u = 2 * math.pow(rho, 1/3)
        y1 = u * math.cos(theta/3)
        y2 = u * math.cos((theta + 2*math.pi)/3)
        y3 = u * math.cos((theta + 4*math.pi)/3)
        roots = [y1 - p3, y2 - p3, y3 - p3]
    
    return tuple(roots)

def matrix_determinant(matrix):
    """
    Calculate the determinant of a matrix.
    
    Args:
        matrix (list of lists): The matrix to calculate the determinant of.
        
    Returns:
        float: The determinant of the matrix.
        
    Example:
        >>> matrix_determinant([[1, 2], [3, 4]])
        -2.0
    """
    n = len(matrix)
    
    if n == 1:
        return matrix[0][0]
    elif n == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    else:
        det = 0
        for j in range(n):
            minor = []
            for i in range(1, n):
                row = []
                for k in range(n):
                    if k != j:
                        row.append(matrix[i][k])
                minor.append(row)
            det += (-1) ** j * matrix[0][j] * matrix_determinant(minor)
        return det
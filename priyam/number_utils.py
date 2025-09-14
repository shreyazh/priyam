"""
Number utilities for common numerical operations.
"""

import math

def is_prime(n):
    """
    Check if a number is prime.
    
    Args:
        n (int): The number to check.
        
    Returns:
        bool: True if the number is prime, False otherwise.
        
    Example:
        >>> is_prime(17)
        True
        >>> is_prime(15)
        False
    """
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    
    return True

def factorial(n):
    """
    Calculate the factorial of a number.
    
    Args:
        n (int): The number to calculate the factorial of.
        
    Returns:
        int: The factorial of the number.
        
    Example:
        >>> factorial(5)
        120
    """
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    if n == 0:
        return 1
    return n * factorial(n - 1)

def fibonacci(n):
    """
    Generate the first n numbers in the Fibonacci sequence.
    
    Args:
        n (int): The number of Fibonacci numbers to generate.
        
    Returns:
        list: The first n Fibonacci numbers.
        
    Example:
        >>> fibonacci(6)
        [0, 1, 1, 2, 3, 5]
    """
    if n <= 0:
        return []
    if n == 1:
        return [0]
    if n == 2:
        return [0, 1]
    
    sequence = [0, 1]
    for i in range(2, n):
        sequence.append(sequence[i-1] + sequence[i-2])
    
    return sequence

def gcd(a, b):
    """
    Calculate the greatest common divisor of two numbers.
    
    Args:
        a (int): The first number.
        b (int): The second number.
        
    Returns:
        int: The greatest common divisor of a and b.
        
    Example:
        >>> gcd(54, 24)
        6
    """
    while b:
        a, b = b, a % b
    return abs(a)

def lcm(a, b):
    """
    Calculate the least common multiple of two numbers.
    
    Args:
        a (int): The first number.
        b (int): The second number.
        
    Returns:
        int: The least common multiple of a and b.
        
    Example:
        >>> lcm(12, 18)
        36
    """
    return abs(a * b) // gcd(a, b) if a and b else 0
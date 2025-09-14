"""
Number theory utilities for advanced mathematical operations.
"""

import math
from sympy import factorint, isprime, primerange, gcd, lcm, mod_inverse
from functools import reduce

def generate_primes(n):
    """
    Generate the first n prime numbers.
    
    Args:
        n (int): The number of primes to generate.
        
    Returns:
        list: The first n prime numbers.
        
    Example:
        >>> generate_primes(5)
        [2, 3, 5, 7, 11]
    """
    primes = []
    num = 2
    while len(primes) < n:
        if is_prime(num):
            primes.append(num)
        num += 1
    return primes

def prime_factorization(n):
    """
    Find the prime factorization of a number.
    
    Args:
        n (int): The number to factorize.
        
    Returns:
        dict: A dictionary with prime factors as keys and exponents as values.
        
    Example:
        >>> prime_factorization(60)
        {2: 2, 3: 1, 5: 1}
    """
    factors = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors[d] = factors.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        factors[n] = factors.get(n, 0) + 1
    return factors

def is_perfect_number(n):
    """
    Check if a number is a perfect number.
    
    Args:
        n (int): The number to check.
        
    Returns:
        bool: True if the number is perfect, False otherwise.
        
    Example:
        >>> is_perfect_number(28)
        True
    """
    if n <= 1:
        return False
    
    divisors = [1]
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            divisors.append(i)
            if i != n // i:
                divisors.append(n // i)
    
    return sum(divisors) == n

def simplify_fraction(numerator, denominator):
    """
    Simplify a fraction to its lowest terms.
    
    Args:
        numerator (int): The numerator of the fraction.
        denominator (int): The denominator of the fraction.
        
    Returns:
        tuple: The simplified fraction as (numerator, denominator).
        
    Example:
        >>> simplify_fraction(8, 12)
        (2, 3)
    """
    if denominator == 0:
        raise ValueError("Denominator cannot be zero")
    
    common_divisor = gcd(numerator, denominator)
    return numerator // common_divisor, denominator // common_divisor

def modular_inverse(a, m):
    """
    Find the modular inverse of a modulo m.
    
    Args:
        a (int): The number to find the inverse of.
        m (int): The modulus.
        
    Returns:
        int: The modular inverse of a modulo m.
        
    Example:
        >>> modular_inverse(3, 11)
        4
    """
    return mod_inverse(a, m)
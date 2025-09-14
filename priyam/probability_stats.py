"""
Probability and statistics utilities for data analysis.
"""

import math
import random
from collections import Counter

def mean(data):
    """
    Calculate the mean of a dataset.
    
    Args:
        data (list): The dataset.
        
    Returns:
        float: The mean of the dataset.
        
    Example:
        >>> mean([1, 2, 3, 4, 5])
        3.0
    """
    return sum(data) / len(data)

def median(data):
    """
    Calculate the median of a dataset.
    
    Args:
        data (list): The dataset.
        
    Returns:
        float: The median of the dataset.
        
    Example:
        >>> median([1, 2, 3, 4, 5])
        3.0
    """
    sorted_data = sorted(data)
    n = len(sorted_data)
    
    if n % 2 == 0:
        return (sorted_data[n//2 - 1] + sorted_data[n//2]) / 2
    else:
        return sorted_data[n//2]

def mode(data):
    """
    Calculate the mode of a dataset.
    
    Args:
        data (list): The dataset.
        
    Returns:
        list: The mode(s) of the dataset.
        
    Example:
        >>> mode([1, 2, 2, 3, 4])
        [2]
    """
    count = Counter(data)
    max_count = max(count.values())
    return [x for x, c in count.items() if c == max_count]

def variance(data, sample=True):
    """
    Calculate the variance of a dataset.
    
    Args:
        data (list): The dataset.
        sample (bool): Whether the data is a sample (True) or population (False).
        
    Returns:
        float: The variance of the dataset.
        
    Example:
        >>> variance([1, 2, 3, 4, 5])
        2.5
    """
    n = len(data)
    if n < 2:
        return 0
    
    m = mean(data)
    sum_sq = sum((x - m) ** 2 for x in data)
    
    if sample:
        return sum_sq / (n - 1)
    else:
        return sum_sq / n

def standard_deviation(data, sample=True):
    """
    Calculate the standard deviation of a dataset.
    
    Args:
        data (list): The dataset.
        sample (bool): Whether the data is a sample (True) or population (False).
        
    Returns:
        float: The standard deviation of the dataset.
        
    Example:
        >>> standard_deviation([1, 2, 3, 4, 5])
        1.5811388300841898
    """
    return math.sqrt(variance(data, sample))

def permutations(n, r):
    """
    Calculate the number of permutations of n items taken r at a time.
    
    Args:
        n (int): Total number of items.
        r (int): Number of items to arrange.
        
    Returns:
        int: The number of permutations.
        
    Example:
        >>> permutations(5, 2)
        20
    """
    if r > n or r < 0:
        return 0
    return math.factorial(n) // math.factorial(n - r)

def combinations(n, r):
    """
    Calculate the number of combinations of n items taken r at a time.
    
    Args:
        n (int): Total number of items.
        r (int): Number of items to choose.
        
    Returns:
        int: The number of combinations.
        
    Example:
        >>> combinations(5, 2)
        10
    """
    if r > n or r < 0:
        return 0
    return math.factorial(n) // (math.factorial(r) * math.factorial(n - r))

def binomial_probability(n, k, p):
    """
    Calculate the binomial probability of k successes in n trials.
    
    Args:
        n (int): Number of trials.
        k (int): Number of successes.
        p (float): Probability of success on a single trial.
        
    Returns:
        float: The binomial probability.
        
    Example:
        >>> binomial_probability(5, 2, 0.5)
        0.3125
    """
    return combinations(n, k) * (p ** k) * ((1 - p) ** (n - k))

def linear_regression(x, y):
    """
    Perform linear regression on a dataset.
    
    Args:
        x (list): The independent variable values.
        y (list): The dependent variable values.
        
    Returns:
        tuple: The slope and intercept of the regression line.
        
    Example:
        >>> linear_regression([1, 2, 3, 4, 5], [2, 4, 5, 4, 5])
        (0.6, 2.2)
    """
    n = len(x)
    if n != len(y):
        raise ValueError("x and y must have the same length")
    
    x_mean = mean(x)
    y_mean = mean(y)
    
    numerator = sum((x[i] - x_mean) * (y[i] - y_mean) for i in range(n))
    denominator = sum((x[i] - x_mean) ** 2 for i in range(n))
    
    if denominator == 0:
        return 0, y_mean
    
    slope = numerator / denominator
    intercept = y_mean - slope * x_mean
    
    return slope, intercept
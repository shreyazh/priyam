
### docs/probability_stats.md
```markdown
# Probability & Statistics Utilities

Functions for statistical analysis and probability calculations.

## Functions

### `mean(data)`

Calculate the mean of a dataset.

**Parameters:**
- `data` (list): The dataset.

**Returns:**
- float: The mean of the dataset.

**Example:**
```python
from priyam.probability_stats import mean

print(mean([1, 2, 3, 4, 5]))  # 3.0

## Functions

### `median(data)`
Calculate the median of a dataset.

**Parameters:**
- `data (list)`: The dataset.

**Returns:**
- `float`: The median of the dataset.

**Example:**
```python
from priyam.probability_stats import median

print(median([1, 2, 3, 4, 5]))  # 3.0
---
from priyam.probability_stats import mode

print(mode([1, 2, 2, 3, 4]))  # [2]
---
from priyam.probability_stats import variance

data = [1, 2, 3, 4, 5]
print(variance(data))  # 2.5 (sample variance)
print(variance(data, sample=False))  # 2.0 (population variance)
---
from priyam.probability_stats import standard_deviation

data = [1, 2, 3, 4, 5]
print(standard_deviation(data))  # 1.5811388300841898
---
from priyam.probability_stats import permutations

print(permutations(5, 2))  # 20
---
from priyam.probability_stats import combinations

print(combinations(5, 2))  # 10
---
from priyam.probability_stats import binomial_probability

print(binomial_probability(5, 2, 0.5))  # 0.3125
---
from priyam.probability_stats import linear_regression

x = [1, 2, 3, 4, 5]
y = [2, 4, 5, 4, 5]
slope, intercept = linear_regression(x, y)
print(f"Slope: {slope}, Intercept: {intercept}")  # Slope: 0.6, Intercept: 2.2


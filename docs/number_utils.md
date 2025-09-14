
### docs/number_utils.md
```markdown
# Number Utilities

Functions for common numerical operations.

## Functions

### `is_prime(n)`

Check if a number is prime.

**Parameters:**
- `n` (int): The number to check.

**Returns:**
- bool: True if the number is prime, False otherwise.

**Example:**
```python
from priyam.number_utils import is_prime

print(is_prime(17))  # True
print(is_prime(15))  # False

---

factorial(n)
Calculate the factorial of a number.

Parameters:

n (int): The number to calculate the factorial of.

Returns:

int: The factorial of the number.

Example:

python
`from priyam.number_utils import factorial

print(factorial(5))  # 120`

---

`fibonacci(n)`
Generate the first n numbers in the Fibonacci sequence.

Parameters:

n (int): The number of Fibonacci numbers to generate.

Returns:

list: The first n Fibonacci numbers.

Example:
`from priyam.number_utils import fibonacci

print(fibonacci(6))  # [0, 1, 1, 2, 3, 5]`

---

`gcd(a, b)`
Calculate the greatest common divisor of two numbers.

Parameters:
a (int): The first number.
b (int): The second number.

Returns:

int: The greatest common divisor of a and b.

Example:
`from priyam.number_utils import gcd

print(gcd(54, 24))  # 6`

---

`lcm(a, b)`
Calculate the least common multiple of two numbers.

Parameters:
a (int): The first number.
b (int): The second number.

Returns:
int: The least common multiple of a and b.

Example:
`from priyam.number_utils import lcm

print(lcm(12, 18))  # 36`

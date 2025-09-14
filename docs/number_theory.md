
### docs/number_theory.md
```markdown
# Number Theory Utilities

Functions for advanced number theory operations.

## Functions

### `generate_primes(n)`

Generate the first n prime numbers.

**Parameters:**
- `n` (int): The number of primes to generate.

**Returns:**
- list: The first n prime numbers.

**Example:**
```python
from priyam.number_theory import generate_primes

print(generate_primes(5))  # [2, 3, 5, 7, 11]

---

`prime_factorization(n)`
Find the prime factorization of a number.

Parameters:
n (int): The number to factorize.

Returns:
dict: A dictionary with prime factors as keys and exponents as values.

Example:
`from priyam.number_theory import prime_factorization

print(prime_factorization(60))  # {2: 2, 3: 1, 5: 1}`

---

`is_perfect_number(n)`
Check if a number is a perfect number.

Parameters:
n (int): The number to check.
Returns:
bool: True if the number is perfect, False otherwise.

Example:
f`rom priyam.number_theory import is_perfect_number

print(is_perfect_number(28))  # True
print(is_perfect_number(10))  # False`

---

`simplify_fraction(numerator, denominator)`
Simplify a fraction to its lowest terms.
Parameters:
`numerator (int): The numerator of the fraction.

denominator (int): The denominator of the fraction.`

Returns:

tuple: The simplified fraction as (numerator, denominator).

Example:
from priyam.number_theory import simplify_fraction

print(simplify_fraction(8, 12))  # (2, 3)

---

`modular_inverse(a, m)`
Find the modular inverse of a modulo m.

Parameters:

a (int): The number to find the inverse of.
m (int): The modulus.

Returns:
int: The modular inverse of a modulo m.

Example:
`from priyam.number_theory import modular_inverse
print(modular_inverse(3, 11))  # 4`
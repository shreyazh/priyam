from typing import Union, List, Callable, Optional
from sympy import Function, dsolve, Derivative, pprint
from sympy import ( symbols, Eq, sympify, solve, diff, integrate, limit, series, Matrix, det, simplify, lambdify, factorint, isprime, primerange, gcd, lcm, mod_inverse)
import math
import random
from collections import Counter
from datetime import datetime
import pytz
import sympy
from dateutil import rrule
import cmath

Number = Union[int, float]

class MathSolver:
    """
    High-level interface for common mathematical tasks.
    Uses sympy for symbolic operations.
    Date and time utilities for common operations.
    Number theory utilities for advanced mathematical operations.
    Probability and statistics utilities for data analysis.
    Number utilities for common numerical operations.
    Algebra utilities for equation solving and symbolic operations.
    """

    @staticmethod
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

    @staticmethod
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
    
    @staticmethod
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

    @staticmethod
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

    @staticmethod
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

    @staticmethod
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

    @staticmethod
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

    @staticmethod
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

    @staticmethod
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

    @staticmethod
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

    @staticmethod
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

    @staticmethod
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

    @staticmethod
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

    @staticmethod
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

    @staticmethod
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

    @staticmethod
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

    @staticmethod
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

    @staticmethod
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

    @staticmethod
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

    @staticmethod
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

    @staticmethod
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

    @staticmethod
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

    @staticmethod
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
        
    @staticmethod
    def simplify_expr(expr: Union[str, "sympy.Expr"]):
        """Simplify a symbolic expression."""
        expr = sympify(expr)
        return simplify(expr)

    @staticmethod
    def solve_equation(
        equation: Union[str, "sympy.Eq"],
        var: Union[str, "sympy.Symbol"]
    ):
        """
        Solve equation = 0 for variable var.

        Examples
        --------
        solve_equation("x**2 - 4", "x")
        solve_equation("sin(x) - x/2", "x")
        """
        if isinstance(equation, str):
            expr = sympify(equation)
            equation = Eq(expr, 0)
        if isinstance(var, str):
            var = symbols(var)
        return solve(equation, var)

    @staticmethod
    def differentiate(expr: Union[str, "sympy.Expr"], var: str, order: int = 1):
        """Differentiate expr wrt var, possibly higher order."""
        var_symbol = symbols(var)
        expr = sympify(expr)
        return diff(expr, var_symbol, order)

    @staticmethod
    def integrate(
        expr: Union[str, "sympy.Expr"],
        var: str,
        lower: Optional[Number] = None,
        upper: Optional[Number] = None,
    ):
        """Compute indefinite or definite integral."""
        var_symbol = symbols(var)
        expr = sympify(expr)
        if lower is None or upper is None:
            return integrate(expr, var_symbol)
        return integrate(expr, (var_symbol, lower, upper))

    @staticmethod
    def compute_limit(expr: Union[str, "sympy.Expr"], var: str, point: Number, dir: str = "+"):
        """Compute limit of expr as var -> point (dir = '+' or '-')."""
        var_symbol = symbols(var)
        expr = sympify(expr)
        return limit(expr, var_symbol, point, dir=dir)

    @staticmethod
    def taylor_series(expr: Union[str, "sympy.Expr"], var: str, a: Number = 0, order: int = 5):
        """
        Taylor series expansion of expr around x = a up to (var - a)**(order - 1).
        """
        var_symbol = symbols(var)
        expr = sympify(expr)
        return series(expr, var_symbol, a, order)

    @staticmethod
    def matrix_from_list(data: List[List[Number]]) -> Matrix:
        return Matrix(data)

    @staticmethod
    def determinant(data: List[List[Number]]):
        """Determinant of a matrix given as nested lists."""
        M = Matrix(data)
        return det(M)

    @staticmethod
    def eigenvalues(data: List[List[Number]]):
        """Symbolic eigenvalues of a matrix."""
        M = Matrix(data)
        return eigenvals(M)

    @staticmethod
    def solve_linear_system(A: List[List[Number]], b: List[Number]):
        """
        Solve Ax = b for x; A is m x n, b is m.
        Returns symbolic solution (may be parametric).
        """
        M = Matrix(A)
        b_vec = Matrix(b)
        return M.gauss_jordan_solve(b_vec)[0]

    # -------- Numeric helpers (wrapping sympy expressions) --------

    @staticmethod
    def numeric_function(
        expr: Union[str, "sympy.Expr"],
        var: str = "x"
    ) -> Callable[[Number], float]:
        """
        Convert a sympy expression to a numeric Python function f(x).
        Useful for plotting, root-finding, etc.
        """
        var_symbol = symbols(var)
        expr = sympify(expr)
        f = lambdify(var_symbol, expr, modules=["math"])
        return lambda x: float(f(x))

    @staticmethod
    def newton_raphson_root(
        expr: Union[str, "sympy.Expr"],
        var: str,
        x0: float,
        tol: float = 1e-8,
        max_iter: int = 100,
    ) -> float:
        """
        Numeric root finder using Newton–Raphson method.
        expr is treated as f(x) = 0.
        """
        x_symbol = symbols(var)
        f_expr = sympify(expr)
        f_prime = diff(f_expr, x_symbol)

        f = lambdify(x_symbol, f_expr, "math")
        df = lambdify(x_symbol, f_prime, "math")

        x = float(x0)
        for _ in range(max_iter):
            fx = f(x)
            dfx = df(x)
            if abs(dfx) < 1e-14:
                break
            x_new = x - fx / dfx
            if abs(x_new - x) < tol:
                return x_new
            x = x_new
        return x

    @staticmethod
    def convert_timezone(dt, from_tz, to_tz):
        """
        Convert a datetime from one timezone to another.
        
        Args:
            dt (datetime): The datetime to convert.
            from_tz (str): The source timezone (e.g., 'UTC', 'US/Eastern').
            to_tz (str): The target timezone (e.g., 'UTC', 'US/Eastern').
            
        Returns:
            datetime: The converted datetime.
            
        Example:
            >>> dt = datetime(2023, 1, 1, 12, 0, 0)
            >>> convert_timezone(dt, 'UTC', 'US/Eastern')
            datetime.datetime(2023, 1, 1, 7, 0, 0, tzinfo=<DstTzInfo 'US/Eastern' EST-1 day, 19:00:00 STD>)
        """
        from_zone = pytz.timezone(from_tz)
        to_zone = pytz.timezone(to_tz)
        
        if dt.tzinfo is None:
            dt = from_zone.localize(dt)
        
        return dt.astimezone(to_zone)

    @staticmethod
    def countdown_timer(end_time):
        """
        Calculate the time remaining until a specified end time.
        
        Args:
            end_time (datetime): The end time to count down to.
            
        Returns:
            dict: A dictionary with days, hours, minutes, and seconds remaining.
            
        Example:
            >>> end_time = datetime.now() + timedelta(days=1, hours=2, minutes=30)
            >>> countdown_timer(end_time)
            {'days': 1, 'hours': 2, 'minutes': 30, 'seconds': 0}
        """
        now = datetime.now(pytz.UTC) if end_time.tzinfo else datetime.now()
        time_remaining = end_time - now
        
        if time_remaining.total_seconds() < 0:
            return {"days": 0, "hours": 0, "minutes": 0, "seconds": 0}
        
        days = time_remaining.days
        seconds = time_remaining.seconds
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        
        return {
            "days": days,
            "hours": hours,
            "minutes": minutes,
            "seconds": seconds
        }

    @staticmethod
    def working_days_calculator(start_date, end_date, holidays=None):
        """
        Calculate the number of working days between two dates.
        
        Args:
            start_date (datetime): The start date.
            end_date (datetime): The end date.
            holidays (list): List of holiday dates to exclude.
            
        Returns:
            int: The number of working days.
            
        Example:
            >>> start = datetime(2023, 1, 1)
            >>> end = datetime(2023, 1, 10)
            >>> working_days_calculator(start, end)
            6
        """
        if holidays is None:
            holidays = []
        
        # Create a rule for weekdays (Monday to Friday)
        rule = rrule.rrule(
            rrule.DAILY,
            byweekday=[rrule.MO, rrule.TU, rrule.WE, rrule.TH, rrule.FR],
            dtstart=start_date,
            until=end_date
        )
        
        # Count working days excluding holidays
        working_days = 0
        for dt in rule:
            if dt.date() not in holidays:
                working_days += 1
        
        return working_days    


class DifferentialEquations:
    """
    Symbolic helpers for ordinary differential equations (ODEs) and simple systems.
    """

    @staticmethod
    def solve_ode(equation: Union[str, "sympy.Eq"], func_name: str, var: str):
        """
        Solve a single ODE symbolically.

        Examples
        --------
        y = Function("y")
        x = symbols("x")
        eq = Eq(Derivative(y(x), x), y(x))     # y' = y
        DifferentialEquations.solve_ode(eq, "y", "x")

        Or string form (for simple cases):
        solve_ode("y'(x) - y(x)", "y", "x")
        """
        if isinstance(equation, str):
            x = symbols(var)
            y = Function(func_name)
            expr = sympify(equation)
            equation = Eq(expr, 0)
        sol = dsolve(equation)
        return sol

    @staticmethod
    def solve_first_order_linear(p: Union[str, "sympy.Expr"],
                                 q: Union[str, "sympy.Expr"],
                                 func_name: str,
                                 var: str):
        """
        Solve y' + p(x) y = q(x).

        Returns: sympy solution.
        """
        x = symbols(var)
        y = Function(func_name)
        p_expr = sympify(p)
        q_expr = sympify(q)
        eq = Eq(Derivative(y(x), x) + p_expr * y(x), q_expr)
        return dsolve(eq)

    @staticmethod
    def solve_system_2x2_linear(a11, a12, a21, a22, b1, b2, var: str = "t"):
        """
        Solve a simple linear system of ODEs:

            x' = a11 x + a12 y + b1
            y' = a21 x + a22 y + b2

        Returns (solution_for_x(t), solution_for_y(t)).
        """
        t = symbols(var)
        x = Function("x")
        y = Function("y")

        eq1 = Eq(Derivative(x(t), t), a11 * x(t) + a12 * y(t) + b1)
        eq2 = Eq(Derivative(y(t), t), a21 * x(t) + a22 * y(t) + b2)

        sol = dsolve((eq1, eq2))
        return sol
    
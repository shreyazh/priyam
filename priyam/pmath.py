from typing import Union, List, Dict, Callable, Optional
from sympy import Function, dsolve, Derivative, pprint
from sympy import (
    symbols, Eq, sympify, solve, diff, integrate, limit, series,
    Matrix, det, eigenvals, simplify, lambdify
)
import math

Number = Union[int, float]


class MathSolver:
    """
    High-level interface for common mathematical tasks.
    Uses sympy for symbolic operations.
    """

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

    # -------- Linear Algebra --------

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
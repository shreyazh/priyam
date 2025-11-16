from typing import Dict
import re
import math

# Minimal periodic table (extend as needed)
PERIODIC_TABLE: Dict[str, float] = {
    "H": 1.008,
    "He": 4.0026,
    "Li": 6.94,
    "Be": 9.0122,
    "B": 10.81,
    "C": 12.011,
    "N": 14.007,
    "O": 15.999,
    "F": 18.998,
    "Ne": 20.180,
    "Na": 22.990,
    "Mg": 24.305,
    "Al": 26.982,
    "Si": 28.085,
    "P": 30.974,
    "S": 32.06,
    "Cl": 35.45,
    "K": 39.098,
    "Ca": 40.078,
    "Fe": 55.845,
    "Cu": 63.546,
    "Zn": 65.38,
    "Br": 79.904,
    "Ag": 107.8682,
    "I": 126.90447,
    "Ba": 137.327,
    "Au": 196.96657,
    "Hg": 200.59,
    "Pb": 207.2,
    # Add more elements as required
}


class ChemistrySolver:
    """
    Fundamental helpers: molar mass, basic stoichiometry.
    """

    @staticmethod
    def molar_mass(formula: str) -> float:
        """
        Compute molar mass of a chemical formula like 'H2O', 'Ca(OH)2', 'C6H12O6'.

        This is a simple parser that supports:
        - element symbols (1 or 2 letters)
        - integer subscripts
        - parentheses with multipliers
        """
        tokens = _tokenize_formula(formula)
        mass, _ = _parse_group(tokens, 0)
        return mass

    @staticmethod
    def grams_to_moles(mass_g: float, formula: str) -> float:
        """n = m / M."""
        M = ChemistrySolver.molar_mass(formula)
        return mass_g / M

    @staticmethod
    def moles_to_grams(moles: float, formula: str) -> float:
        """m = n M."""
        M = ChemistrySolver.molar_mass(formula)
        return moles * M

    @staticmethod
    def ideal_gas_volume(n_moles: float, T_K: float, P_Pa: float) -> float:
        """
        Compute volume from ideal gas law: PV = nRT.
        Returns volume in m^3.
        """
        R = 8.3145  # J/(mol K)
        return n_moles * R * T_K / P_Pa


# ---------- Internal formula parser ----------

TOKEN_PATTERN = re.compile(
    r"([A-Z][a-z]?)|(\()|(\))|(\d+)"
)


def _tokenize_formula(formula: str):
    tokens = []
    for match in TOKEN_PATTERN.finditer(formula):
        element, lpar, rpar, number = match.groups()
        if element:
            tokens.append(("ELEM", element))
        elif lpar:
            tokens.append(("LPAR", lpar))
        elif rpar:
            tokens.append(("RPAR", rpar))
        elif number:
            tokens.append(("NUM", int(number)))
    return tokens


def _parse_group(tokens, i: int):
    """
    Recursive descent parser for group ::=
        ( element [num] | '(' group ')' [num] )+
    Returns (mass, new_index).
    """
    total_mass = 0.0
    while i < len(tokens):
        token_type, value = tokens[i]
        if token_type == "ELEM":
            elem = value
            if elem not in PERIODIC_TABLE:
                raise ValueError(f"Unknown element: {elem}")
            atomic_mass = PERIODIC_TABLE[elem]
            i += 1
            # optional number
            if i < len(tokens) and tokens[i][0] == "NUM":
                count = tokens[i][1]
                i += 1
            else:
                count = 1
            total_mass += atomic_mass * count
        elif token_type == "LPAR":
            # parse sub-group
            sub_mass, i = _parse_group(tokens, i + 1)
            # expect closing parenthesis
            if i >= len(tokens) or tokens[i][0] != "RPAR":
                raise ValueError("Unmatched '(' in formula.")
            i += 1
            # optional multiplier
            if i < len(tokens) and tokens[i][0] == "NUM":
                mult = tokens[i][1]
                i += 1
            else:
                mult = 1
            total_mass += sub_mass * mult
        elif token_type == "RPAR":
            # caller is responsible for consuming RPAR
            break
        else:
            raise ValueError(f"Unexpected token {token_type} at position {i}")
    return total_mass, i

class Equilibrium:
    """
    Simple equilibrium and acid-base helpers.
    Idealized; assumes activities ≈ concentrations.
    """

    @staticmethod
    def henderson_hasselbalch(pKa: float, base_conc: float, acid_conc: float) -> float:
        """
        pH = pKa + log10([base]/[acid]).
        For buffer solutions (weak acid / conjugate base).
        """
        if acid_conc <= 0 or base_conc <= 0:
            raise ValueError("Concentrations must be positive.")
        return pKa + math.log10(base_conc / acid_conc)

    @staticmethod
    def pH_strong_acid(C: float) -> float:
        """
        pH of a strong monoprotic acid: [H+] = C.
        """
        if C <= 0:
            raise ValueError("Concentration must be positive.")
        return -math.log10(C)

    @staticmethod
    def pH_strong_base(C: float) -> float:
        """
        pH of a strong monoprotic base: [OH-] = C.
        Kw = 1.0e-14 at 25°C.
        """
        if C <= 0:
            raise ValueError("Concentration must be positive.")
        Kw = 1.0e-14
        h_plus = Kw / C
        return -math.log10(h_plus)

    @staticmethod
    def weak_acid_pH(C: float, Ka: float) -> float:
        """
        Approximate pH of weak monoprotic acid HA with initial conc C:
        HA ⇌ H+ + A-
        Assume x << C: [H+] ≈ sqrt(Ka * C).
        """
        if C <= 0 or Ka <= 0:
            raise ValueError("C and Ka must be positive.")
        h_plus = math.sqrt(Ka * C)
        return -math.log10(h_plus)

    @staticmethod
    def equilibrium_concentration_aA_bB_cC_dD(
        K: float,
        a: int,
        b: int,
        c: int,
        d: int,
        A0: float,
        B0: float,
        C0: float = 0.0,
        D0: float = 0.0,
    ):
        """
        Very simple 1D extent-of-reaction approach for:
            a A + b B ⇌ c C + d D

        Assumes single reaction extent ξ and uses numeric search.
        This is illustrative and not a robust solver for all cases.
        """
        from sympy import symbols, Eq, nsolve

        xi = symbols("xi")
        A = A0 - a * xi
        B = B0 - b * xi
        C = C0 + c * xi
        D = D0 + d * xi

        # Avoid division by zero: K = [C]^c [D]^d / ([A]^a [B]^b)
        # Use symbolic equation:
        eq = Eq((C ** c) * (D ** d) / ((A ** a) * (B ** b)), K)

        guess = min(A0 / max(a, 1), B0 / max(b, 1)) / 2
        sol = nsolve(eq, xi, guess)

        A_eq = float(A.subs(xi, sol))
        B_eq = float(B.subs(xi, sol))
        C_eq = float(C.subs(xi, sol))
        D_eq = float(D.subs(xi, sol))
        return {"A": A_eq, "B": B_eq, "C": C_eq, "D": D_eq}

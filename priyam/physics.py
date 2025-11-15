from typing import Union, Tuple
import math

Number = Union[int, float]

class Kinematics:
    """
    Standard 1D kinematics under constant acceleration.
    """

    @staticmethod
    def final_velocity(u: Number, a: Number, t: Number) -> float:
        """v = u + a t"""
        return float(u + a * t)

    @staticmethod
    def displacement(u: Number, t: Number, a: Number = 0) -> float:
        """s = u t + 0.5 a t^2"""
        return float(u * t + 0.5 * a * t * t)

    @staticmethod
    def final_velocity_squared(u: Number, a: Number, s: Number) -> float:
        """v^2 = u^2 + 2 a s"""
        return float(u * u + 2 * a * s)

    @staticmethod
    def time_from_displacement(u: Number, a: Number, s: Number) -> Tuple[float, float]:
        """
        Solve s = u t + 1/2 a t^2 for t.
        Returns both roots (could be complex if discriminant < 0).
        """
        A = 0.5 * a
        B = u
        C = -s
        disc = B * B - 4 * A * C
        if disc < 0:
            # complex roots
            sqrt_disc = complex(0, math.sqrt(-disc))
        else:
            sqrt_disc = math.sqrt(disc)
        t1 = (-B + sqrt_disc) / (2 * A)
        t2 = (-B - sqrt_disc) / (2 * A)
        return float(t1), float(t2)


class Dynamics:
    """
    Newtonian dynamics helpers.
    """

    @staticmethod
    def force(mass: Number, acceleration: Number) -> float:
        """F = m a"""
        return float(mass * acceleration)

    @staticmethod
    def weight(mass: Number, g: Number = 9.81) -> float:
        """Weight = m g"""
        return float(mass * g)

    @staticmethod
    def momentum(mass: Number, velocity: Number) -> float:
        """p = m v"""
        return float(mass * velocity)

    @staticmethod
    def kinetic_energy(mass: Number, velocity: Number) -> float:
        """K = 1/2 m v^2"""
        return float(0.5 * mass * velocity * velocity)

    @staticmethod
    def potential_energy(mass: Number, height: Number, g: Number = 9.81) -> float:
        """U = m g h"""
        return float(mass * g * height)


class ProjectileMotion:
    """
    Ideal projectile motion in uniform gravity, no air resistance.
    Angles in radians.
    """

    @staticmethod
    def time_of_flight(u: Number, theta: Number, g: Number = 9.81) -> float:
        """T = 2 u sin(theta) / g"""
        return float(2 * u * math.sin(theta) / g)

    @staticmethod
    def range(u: Number, theta: Number, g: Number = 9.81) -> float:
        """R = u^2 sin(2 theta) / g"""
        return float((u ** 2) * math.sin(2 * theta) / g)

    @staticmethod
    def max_height(u: Number, theta: Number, g: Number = 9.81) -> float:
        """H = u^2 sin^2(theta) / (2 g)"""
        return float((u ** 2) * (math.sin(theta) ** 2) / (2 * g))


class WavesOptics:
    """
    Simple wave and optics relations.
    """

    @staticmethod
    def wave_speed(frequency: Number, wavelength: Number) -> float:
        """v = f λ"""
        return float(frequency * wavelength)

    @staticmethod
    def snell_law(n1: Number, n2: Number, theta1: Number) -> float:
        """
        Compute refraction angle theta2 using Snell's law:
        n1 sin(theta1) = n2 sin(theta2)
        Returns theta2 in radians.
        """
        sin_theta2 = n1 * math.sin(theta1) / n2
        if abs(sin_theta2) > 1:
            raise ValueError("Total internal reflection (no real refraction angle).")
        return float(math.asin(sin_theta2))

class Electromagnetism:
    """
    Basic electrostatics and magnetostatics formula helpers.
    SI units assumed (C, m, N, etc.).
    """

    K_E = 8.9875517923e9  # Coulomb constant (N m^2 / C^2)
    MU_0 = 4 * math.pi * 1e-7  # vacuum permeability (N/A^2)

    @staticmethod
    def coulomb_force(q1: Number, q2: Number, r: Number) -> float:
        """
        Magnitude of the electrostatic force between two point charges:
        F = k_e * |q1 q2| / r^2
        """
        if r == 0:
            raise ValueError("Distance r must be nonzero.")
        return float(Electromagnetism.K_E * abs(q1 * q2) / (r ** 2))

    @staticmethod
    def electric_field_point_charge(q: Number, r: Number) -> float:
        """
        Magnitude of electric field of point charge:
        E = k_e * |q| / r^2
        """
        if r == 0:
            raise ValueError("Distance r must be nonzero.")
        return float(Electromagnetism.K_E * abs(q) / (r ** 2))

    @staticmethod
    def magnetic_field_long_wire(I: Number, r: Number) -> float:
        """
        Magnetic field magnitude at distance r from a long straight wire:
        B = μ0 I / (2π r)
        """
        if r == 0:
            raise ValueError("Distance r must be nonzero.")
        return float(Electromagnetism.MU_0 * I / (2 * math.pi * r))

    @staticmethod
    def lorentz_force(q: Number, v: Number, B: Number, theta: Number) -> float:
        """
        Magnitude of magnetic Lorentz force:
        F = |q| v B sin(theta)
        """
        return float(abs(q) * v * B * math.sin(theta))


class Thermodynamics:
    """
    Basic thermodynamics: ideal gas processes, heat, work.
    """

    R = 8.3145  # J/mol K

    @staticmethod
    def work_isobaric(P: Number, dV: Number) -> float:
        """W = P ΔV (isobaric process)."""
        return float(P * dV)

    @staticmethod
    def work_isothermal(n: Number, T: Number, V1: Number, V2: Number) -> float:
        """
        Isothermal expansion/compression (ideal gas):
        W = n R T ln(V2 / V1)
        """
        if V1 <= 0 or V2 <= 0:
            raise ValueError("Volumes must be positive.")
        return float(n * Thermodynamics.R * T * math.log(V2 / V1))

    @staticmethod
    def internal_energy_change_ideal(n: Number, Cv: Number, dT: Number) -> float:
        """
        ΔU = n Cv ΔT (for ideal gas).
        Cv in J/mol K.
        """
        return float(n * Cv * dT)

    @staticmethod
    def heat_added(dU: Number, W_by_system: Number) -> float:
        """
        First law: ΔU = Q - W (by system).
        Given ΔU and W(by system), find Q.
        """
        return float(dU + W_by_system)

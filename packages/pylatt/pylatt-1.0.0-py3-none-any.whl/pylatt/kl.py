#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Benjamin Vial
# License: MIT


"""
Arrangement of spring-mass resonators attached to a thin elastic layer.

[Torrent2013]: Daniel Torrent, Didier Mayou and José Sánchez-Dehesa1, 
Elastic analog of graphene: Dirac cones and edge states for flexural waves in thin plates
PHYSICAL REVIEW B 87, 115143 (2013)
"""

import functools
import time

import pylatt

from . import get_backend, logger

backend = get_backend()

from dataclasses import dataclass

import numpy as np
import scipy.special as sp

from . import backend as bk


def timer(func):
    """Print the runtime of the decorated function"""

    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_time = time.perf_counter()  # 1
        value = func(*args, **kwargs)
        end_time = time.perf_counter()  # 2
        run_time = end_time - start_time  # 3
        logger.debug(f"Finished {func.__name__!r} in {run_time:.4f} s")
        return value

    return wrapper_timer


EPS = 1e-12


def j0(kr):
    return sp.jn(0, kr)


def j1(kr):
    return sp.jn(1, kr)


def y0(kr):
    return sp.yv(0, kr)


def y1(kr):
    return sp.yv(1, kr)


def k0(kr):
    return sp.kv(0, kr)


def k1(kr):
    return sp.kv(1, kr)


bessel_j0 = bk.special.bessel_j0 if backend == "torch" else j0
bessel_y0 = bk.special.bessel_y0 if backend == "torch" else y0
bessel_k0 = bk.special.modified_bessel_k0 if backend == "torch" else k0
bessel_j1 = bk.special.bessel_j1 if backend == "torch" else j1
bessel_y1 = bk.special.bessel_y1 if backend == "torch" else y1
bessel_k1 = bk.special.modified_bessel_k1 if backend == "torch" else k1


def switch_complex(f1, f2):
    def wrapper(z):
        if np.all(np.iscomplex(z)):
            return f2(z)
        return f1(z.real)

    return wrapper


bessel_j0 = switch_complex(bessel_j0, j0)
bessel_y0 = switch_complex(bessel_y0, y0)
bessel_k0 = switch_complex(bessel_k0, k0)
bessel_j1 = switch_complex(bessel_j1, j1)
bessel_y1 = switch_complex(bessel_y1, y1)
bessel_k1 = switch_complex(bessel_k1, k1)


@dataclass
class Pin:
    """Class representing a pin."""

    position: tuple

    def strength(self, omega) -> float:
        return 1


@dataclass
class Mass:
    """Class representing a mass."""

    mass: float
    position: tuple

    def strength(self, omega) -> float:
        """t_alpha * D in [Torrent2013]"""
        return self.mass * omega**2


@dataclass
class Resonator:
    """Class representing a resonator."""

    mass: float
    stiffness: float
    position: tuple

    @property
    def omega_r(self) -> float:
        return (self.stiffness / self.mass) ** 0.5

    def strength(self, omega) -> float:
        """t_alpha * D in [Torrent2013]"""
        return (
            self.mass
            * self.omega_r**2
            * omega**2
            / (self.omega_r**2 - omega**2)
        )


@dataclass
class ElasticPlate:
    """Class representing a thin elastic plate."""

    rho: float  # mass density
    h: float  # thickness
    E: float  # Young's modulus
    nu: float  # Poisson ratio

    @property
    def bending_stiffness(self) -> float:
        return self.E * self.h**3 / (12 * (1 - self.nu**2))


def _gfreal(kr):
    return bk.where(bk.abs(kr) < EPS, 1.0, bessel_j0(kr))


def _gfimag(kr):
    return bk.where(
        bk.abs(kr) < EPS,
        0.0,
        bessel_y0(kr) + 2 / bk.pi * bessel_k0(kr),
    )


def _dgfreal(kr):
    return bk.where(bk.abs(kr) < EPS, 0.0, -bessel_j1(kr))


def _dgfimag(kr):
    return bk.where(
        bk.abs(kr) < EPS,
        0.0,
        -bessel_y1(kr) - 2 / bk.pi * bessel_k1(kr),
    )


if backend == "torch":

    class GFreal(bk.autograd.Function):
        @staticmethod
        def forward(ctx, kr):
            ctx.save_for_backward(kr)
            return _gfreal(kr)

        @staticmethod
        def backward(ctx, grad_output):
            (kr,) = ctx.saved_tensors
            return grad_output * _dgfreal(kr)

    class GFimag(bk.autograd.Function):
        @staticmethod
        def forward(ctx, kr):
            ctx.save_for_backward(kr)
            return _gfimag(kr)

        @staticmethod
        def backward(ctx, grad_output):
            (kr,) = ctx.saved_tensors
            return grad_output * _dgfimag(kr)

    gfreal = GFreal.apply
    gfimag = GFimag.apply
else:
    gfreal = _gfreal
    gfimag = _gfimag


def greens_function(k, r):
    kr = k * r
    return 1j / (8 * k**2) * (gfreal(kr) + 1j * gfimag(kr))


def _radial_coord(x, y):
    return (EPS + x**2 + y**2) ** 0.5


class ScatteringSimulation:
    def __init__(self, plate, res_array):
        self.plate = plate
        self.res_array = res_array

    @property
    def n_res(self):
        return len(self.res_array)

    def _strength(self, omega, resonator):
        """T_alpha in [Torrent2013]"""
        k = self.wavenumber(omega)
        if isinstance(resonator, Pin):
            return 1j * 8 * k**2
        t_alpha = resonator.strength(omega) / self.plate.bending_stiffness
        return t_alpha / (1 - 1j * t_alpha / (8 * k**2))

    def wavenumber(self, omega):
        return (
            omega**0.5
            * (self.plate.rho * self.plate.h / self.plate.bending_stiffness) ** 0.25
        )

    def plane_wave(self, x, y, omega, angle):
        k = self.wavenumber(omega)
        return bk.exp(1j * k * (bk.cos(angle) * x + bk.sin(angle) * y))

    def line_source(self, x, y, omega, position):
        k = self.wavenumber(omega)
        xs, ys = position
        r = _radial_coord(x - xs, y - ys)
        return greens_function(k, r)

    @timer
    def build_vector(self, phi0, omega, *args, **kwargs):
        phi0_vec = bk.array(bk.zeros((self.n_res), dtype=bk.complex128))
        for alpha, res_alpha in enumerate(self.res_array):
            xalpha, yalpha = res_alpha.position
            phi0_vec[alpha] = phi0(xalpha, yalpha, omega, *args, **kwargs)

        return phi0_vec

    @timer
    def build_matrix(self, omega):
        k = self.wavenumber(omega)
        matrix = bk.array(bk.zeros((self.n_res, self.n_res), dtype=bk.complex128))
        for alpha, res_alpha in enumerate(self.res_array):
            xalpha, yalpha = res_alpha.position
            for beta, res_beta in enumerate(self.res_array):
                xbeta, ybeta = res_beta.position
                delta = 1 if alpha == beta else 0
                dr = _radial_coord(xalpha - xbeta, yalpha - ybeta)
                G0 = greens_function(k, dr)
                T_beta = self._strength(omega, res_beta)
                matrix[alpha, beta] = delta - (1 - delta) * T_beta * G0
        return matrix

    @timer
    def get_external_field(self, phi0, phie_beta, omega, *args, **kwargs):
        k = self.wavenumber(omega)
        phie_alpha = bk.zeros((self.n_res), dtype=bk.complex128)
        for alpha, res_alpha in enumerate(self.res_array):
            xalpha, yalpha = res_alpha.position
            phie_alpha[alpha] = phi0(xalpha, yalpha, omega, *args, **kwargs)
            for beta, res_beta in enumerate(self.res_array):
                if alpha != beta:
                    xbeta, ybeta = res_beta.position
                    dr = _radial_coord(xalpha - xbeta, yalpha - ybeta)
                    G0 = greens_function(k, dr)
                    T_beta = self._strength(omega, res_beta)
                    phie_alpha[alpha] += T_beta * phie_beta[beta] * G0
        return phie_alpha

    @timer
    def solve(self, phi0, omega, *args, **kwargs):
        """Solve the multiple scattering problem

        Parameters
        ----------
        phi0 : callable
            The incident field. Signature should be phi0(x, y, omega, *args, **kwargs).
        """
        phi0_vec = bk.array(bk.zeros((self.n_res), dtype=bk.complex128))
        matrix = self.build_matrix(omega)
        phi0_vec = self.build_vector(phi0, omega, *args, **kwargs)
        phie_beta = self.solve_phie_beta(matrix, phi0_vec)
        return self.get_external_field(phi0, phie_beta, omega, *args, **kwargs)

    @timer
    def solve_phie_beta(self, matrix, phi0_vec):
        return bk.linalg.solve(matrix, phi0_vec)

    @timer
    def get_field(self, x, y, phi0, phie_alpha, omega, *args, **kwargs):
        k = self.wavenumber(omega)
        W = phi0(x, y, omega, *args, **kwargs)
        for alpha, res_alpha in enumerate(self.res_array):
            xalpha, yalpha = res_alpha.position
            T_alpha = self._strength(omega, res_alpha)
            dr = _radial_coord(x - xalpha, y - yalpha)
            G0 = greens_function(k, dr)
            W += T_alpha * phie_alpha[alpha] * G0
        return W

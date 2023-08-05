#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Benjamin Vial
# This file is part of pylatt
# License: GPLv3
# See the documentation at benvial.gitlab.io/pylatt

import sys

sys.path.append("examples")


def test_1D():
    import pylatt as pl

    nodes = [pl.Node(0, 1), pl.Node(1, 3)]
    beams = [pl.Beam(0, 1, 1)]

    lat = pl.Lattice(1, nodes, beams, space_dim=1)
    lat.eigensolve(0)
    lat.plot()

    nodes = [pl.Node(0, 1), pl.Node(10, 3)]
    beams = [pl.Beam(0, 10, 1)]
    lat = pl.LatticeFinite(nodes, beams, space_dim=1)
    lat.eigensolve()


def test_2D():
    import pylatt as pl

    nodes = [pl.Node((0, 0), 1), pl.Node((0, 1), 1)]
    beams = [pl.Beam((0, 0), (0, 1), 1)]

    lat = pl.Lattice(((1, 0), (0, 1)), nodes, beams)
    w, v = lat.eigensolve((0, 0))
    lat.plot()
    lat = pl.LatticeFinite(nodes, beams)
    lat.eigensolve()
    w, v = lat.eigensolve()
    lat.plot()
    lat.plot_deform(w, v[0])


def test_biatomic_triangular_lattice():
    import plot_biatomic_triangular_lattice


def test_square_frame():
    import plot_square_frame

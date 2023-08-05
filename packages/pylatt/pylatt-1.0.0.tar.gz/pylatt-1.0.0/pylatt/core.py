#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Benjamin Vial
# This file is part of pylatt
# License: GPLv3
# See the documentation at benvial.gitlab.io/pylatt

import glob
import os
import tempfile
from itertools import accumulate

import matplotlib.pyplot as plt
import tqdm
from PIL import Image

from . import backend as bk


def copy(x):
    return bk.clone(x) if bk.__name__ == "torch" else bk.copy(x)


def progbar(x, desc=None, use=True):
    if use:
        return tqdm.tqdm(x, desc=desc, colour="red")
    else:
        return x


def is_hermitian(M):
    return bk.allclose(M, M.T.conj())


def eig(A, B, vectors=True):
    M = bk.linalg.solve(B, A)
    if vectors:
        _eig = bk.linalg.eigh if is_hermitian(M) else bk.linalg.eig
    else:
        _eig = bk.linalg.eigvalsh if is_hermitian(M) else bk.linalg.eigvals

    return _eig(M)


def Atruss(axial_stiffness, unit_vector, dim=2):
    if dim == 1:
        return bk.array([axial_stiffness, -axial_stiffness])
    else:
        # if dim == 2:
        u = bk.tile(unit_vector, (1, 1))
        aa = u.T @ u
        return axial_stiffness * bk.stack([bk.stack([aa, -aa]), bk.stack([-aa, aa])])
    # else:

    #     u = bk.tile(unit_vector, (1, 1))
    #     aa = u.T @ u
    #     return axial_stiffness * bk.stack(
    #         [
    #             bk.stack([aa, -aa, -aa]),
    #             bk.stack([-aa, aa, -aa]),
    #             bk.stack([-aa, -aa, aa]),
    #         ]
    #     )


def _build_torch_array(list):
    A = bk.array(bk.zeros((3, 3)), dtype=bk.float64)
    for i in range(3):
        for j in range(3):
            A[i, j] = list[i][j]
    return A


def Aframe(axial_stiffness, bending_stiffness, unit_vector, dim=2):
    c, d = axial_stiffness, bending_stiffness
    cos, sin = unit_vector
    R = _build_torch_array([[cos, -sin, 0], [sin, cos, 0], [0, 0, 1]])

    A11 = _build_torch_array([[c, 0, 0], [0, d, d / 2], [0, d / 2, d / 3]])

    A12 = _build_torch_array([[-c, 0, 0], [0, -d, d / 2], [0, -d / 2, d / 6]])

    A21 = A12.T.conj()

    A22 = _build_torch_array([[c, 0, 0], [0, d, -d / 2], [0, -d / 2, d / 3]])
    # A22 = A11
    RT = R.T
    A11 = R @ A11 @ RT
    A12 = R @ A12 @ RT
    A22 = R @ A22 @ RT
    A21 = R @ A21 @ RT
    # A21 = A12.T.conj()
    return bk.stack([bk.stack([A11, A12]), bk.stack([A21, A22])])


def delta(i, j):
    return 1 if i == j else 0


def xn(basis_vectors, n, dim=2):
    if dim == 1:
        out = basis_vectors * n
    else:
        out = basis_vectors.T @ bk.array(n, dtype=bk.float64)
    return out


def phasor(k, basis_vectors, n, dim=2):
    if dim == 1:
        return bk.exp(-1j * xn(basis_vectors, n, dim) * k)

    else:
        return bk.exp(
            -1j * bk.dot(xn(basis_vectors, n, dim), bk.array(k, dtype=bk.float64))
        )


def _get_A(member, case, dim=2):
    if case == "truss":
        return Atruss(member.bar.axial_stiffness, member.unit_vector, dim)
    else:
        return Aframe(
            member.bar.axial_stiffness,
            member.bar.bending_stiffness,
            member.unit_vector,
            dim,
        )


def _sigma(
    i,
    j,
    k,
    index_set,
    member_set,
    member_set_extra,
    basis_vectors,
    case,
    dim,
):
    s = 0
    for node, member in zip(index_set, member_set):
        m = node.cell
        ph = phasor(k, basis_vectors, m, dim)
        A = _get_A(member, case, dim)
        if dim == 1:
            s += A[0] * delta(i, j) + ph * A[1]

        else:
            s += A[0, 0] * delta(i, j) + ph * A[0, 1]

    for member1 in member_set_extra:
        A1 = _get_A(member1, case, dim)
        if dim == 1:
            s += A1[0] * delta(i, j)

        else:
            s += A1[0, 0] * delta(i, j)

    return s


def _allclose(a, b, tol=1e-12):
    try:
        for _a, _b in zip(a, b):
            if abs(_a - _b) > tol:
                return False
    except:
        if abs(a - b) > tol:
            return False
    return True


class _Node:
    """A node."""

    def __init__(self, index, coordinates, mass, moment=0, cell=(0, 0)):
        self.index = index
        self.coordinates = bk.array(coordinates, dtype=bk.float64)
        self.mass = mass
        self.moment = moment
        self.cell = bk.array(cell, dtype=bk.float64)

    def __repr__(self):
        return f"Node(index {self.index}, coords {self.coordinates}, mass {self.mass}, moment {self.moment}, cell {self.cell})"

    # def is_reference(self):
    #     return self.cell == (0, 0)

    def connects_to(self, node, beam):
        cond1 = _allclose(self.coordinates, beam.start) and _allclose(
            node.coordinates, beam.end
        )
        cond2 = _allclose(self.coordinates, beam.end) and _allclose(
            node.coordinates, beam.start
        )
        return cond1 or cond2

    def __eq__(self, other):
        return (
            self.moment == other.moment
            and _allclose(self.cell, other.cell)
            and self.mass == other.mass
            and self.index == other.index
            and _allclose(self.coordinates, other.coordinates)
        )

    def copy(self):
        return _Node(self.index, self.coordinates, self.mass, self.moment, self.cell)


class Node:
    """A node."""

    def __init__(self, coordinates, mass, moment=0):
        self.coordinates = bk.array(coordinates, dtype=bk.float64)
        self.mass = mass
        self.moment = moment

    def __repr__(self):
        return (
            f"Node(coords {self.coordinates}, mass {self.mass}, moment {self.moment})"
        )


class Beam:
    """A beam."""

    def __init__(self, start, end, axial_stiffness, bending_stiffness=0):
        if isinstance(start, Node):
            start = start.coordinates
        if isinstance(end, Node):
            end = end.coordinates
        self.start = bk.array(start, dtype=bk.float64)
        self.end = bk.array(end, dtype=bk.float64)
        self.axial_stiffness = axial_stiffness
        self.bending_stiffness = bending_stiffness

    @property
    def length(self):
        return bk.linalg.norm(self.end - self.start)

    @property
    def bar(self):
        return Bar(self.length, self.axial_stiffness, self.bending_stiffness)

    def __repr__(self):
        return f"Beam(start {self.start}, end {self.end}, c {self.axial_stiffness}, d {self.bending_stiffness})"

    def copy(self):
        return Beam(self.start, self.end, self.axial_stiffness, self.bending_stiffness)


class Bar:
    """A bar."""

    def __init__(self, length, axial_stiffness, bending_stiffness=0):
        self.length = length
        self.axial_stiffness = axial_stiffness
        self.bending_stiffness = bending_stiffness

    def __repr__(self):
        return f"Bar(length {self.length}, c {self.axial_stiffness}, d {self.bending_stiffness})"

    def __eq__(self, other):
        return (
            self.length == other.length
            and self.axial_stiffness == other.axial_stiffness
            and self.bending_stiffness == other.bending_stiffness
        )


class Member:
    """A member."""

    def __init__(self, node0, node1, bar):
        self.node0 = node0
        self.node1 = node1
        self.bar = bar
        direction = bk.array(node1.coordinates) - bk.array(node0.coordinates)
        self.unit_vector = direction / bk.linalg.norm(direction)

    def __eq__(self, other):
        return (
            self.node0 == other.node0
            and self.node1 == other.node1
            and self.bar == other.bar
        )

    def __repr__(self):
        return f"Member(nodes ({self.node0},{self.node1}), bar {self.bar}, u {self.unit_vector})"


class Lattice:
    """A lattice object defining the unit cell."""

    def __init__(
        self,
        basis_vectors,
        nodes,
        beams,
        case="truss",
        space_dim=2,
        progress=False,
        max_members=None,
    ):
        self.space_dim = space_dim
        self.max_members = max_members
        self.beams = beams
        self.basis_vectors = bk.array(basis_vectors, dtype=bk.float64)
        self.case = case
        self.progress = progress
        self.nodes = self._init_nodes(nodes)
        self.members = self._find_members()

        if space_dim == 1:
            if case == "frame":
                raise ValueError("frame only valid for space_dim>1")
            else:
                self.n_dof = 1
        elif space_dim == 2:
            self.n_dof = 2 if case == "truss" else 3
        elif space_dim == 3:
            self.n_dof = 3 if case == "truss" else 9
        else:
            raise NotImplementedError("space_dim must be 1 or 2")

        self.dim = self.n_dof * self.num_nodes
        self.masses = [s.mass for s in self.nodes]
        self.moments = [s.moment for s in self.nodes]
        # TODO: speedup search for member_set_list
        self.member_set_list = [
            [self.member_set(i, j) for j in range(self.num_nodes)]
            for i in range(self.num_nodes)
        ]

        self.index_set_list = [
            [
                [m.node1 for m in self.member_set_list[i][j]]
                for j in range(self.num_nodes)
            ]
            for i in range(self.num_nodes)
        ]
        self.member_set_list_extra = [
            [self.get_member_set_extra(i, j) for j in range(self.num_nodes)]
            for i in range(self.num_nodes)
        ]

        # self.index_set_list1 = [
        #     [self.get_indes_set_extra(i, j) for j in range(self.num_nodes)]
        #     for i in range(self.num_nodes)
        # ]

    def _init_nodes(self, nodes):
        _nodes = []
        if self.space_dim == 1:
            cell = 0
        elif self.space_dim == 2:
            cell = (0, 0)
        else:
            cell = (0, 0, 0)
        for i, node in enumerate(nodes):
            _nodes.append(_Node(i, node.coordinates, node.mass, node.moment, cell=cell))
        return _nodes

    def _find_members(self):
        """Find members by looking at adjacent unit cells"""

        # TODO: speedup member search

        nodes = self.nodes
        beams = self.beams

        if self.space_dim == 1:
            cells = bk.array([i for i in range(-1, 2)], dtype=bk.float64)
        elif self.space_dim == 2:
            cells = bk.array(
                [(i, j) for j in range(-1, 2) for i in range(-1, 2)], dtype=bk.float64
            )
        else:
            # raise NotImplementedError()
            cells = bk.array(
                [
                    (i, j, k)
                    for k in range(-1, 2)
                    for j in range(-1, 2)
                    for i in range(-1, 2)
                ],
                dtype=bk.float64,
            )

        v = self.basis_vectors
        _members = []

        tnodes = progbar(nodes, desc="Finding members", use=self.progress)
        for node0 in tnodes:
            for c in cells:
                shifted_coord = (
                    v * c if self.space_dim == 1 else bk.inner(v.T, c)
                )  # v[0]*c[0]+v[1]*c[1]#v@c

                for node1 in nodes:
                    node1 = node1.copy()
                    node1.coordinates = bk.array(node1.coordinates) + shifted_coord
                    node1.cell = c
                    for beam in beams.copy():
                        beam = beam.copy()
                        if node0.connects_to(node1, beam):
                            m = Member(node0, node1, beam.bar)
                            if m not in _members:
                                _members.append(m)
                    for beam in beams.copy():
                        beam = beam.copy()
                        b_coord = bk.vstack([beam.start, beam.end])
                        b_coord += bk.vstack([shifted_coord])
                        beam.start = b_coord[0]
                        beam.end = b_coord[1]
                        if node0.connects_to(node1, beam):
                            m = Member(node0, node1, beam.bar)
                            if m not in _members:
                                _members.append(m)
        return _members

    @property
    def num_nodes(self):
        return len(self.nodes)

    @property
    def num_members(self):
        return len(self.members)

    @property
    def reciprocal_vectors(self):
        return 2 * bk.pi * bk.linalg.inv(bk.array(self.basis_vectors).T)

    def member_set(self, i, j):
        out = []
        for m in self.members:
            # print(m)
            if self.max_members is not None:
                if len(out) >= self.max_members:
                    # print("maximum members reached!")
                    break
            if m.node0 == self.nodes[i] and m.node1.index == j:
                out.append(m)
        return out

    def member_set_indices(self, i, j):
        out = []
        k = 0
        for m in self.members:
            # print(m)
            if self.max_members is not None:
                if len(out) >= self.max_members:
                    # print("maximum members reached!")
                    break
            if m.node0 == self.nodes[i] and m.node1.index == j:
                out.append(k)
            k += 1
        return out

    def index_set(self, i, j):
        return [m.node1 for m in self.member_set(i, j)]

    def get_member_set_extra(self, i, j):
        _member_set_extra = []
        for j1 in range(self.num_nodes):
            if j1 != j:
                _member_set_extra += self.member_set_list[i][j1]
        return _member_set_extra

    # def get_indes_set_extra(self, i, j):
    #     _indes_set_extra = []
    #     for j1 in range(self.num_nodes):
    #         if j1 != j:
    #             _indes_set_extra += self.index_set_list[i][j1]
    #     return _indes_set_extra

    def _sigma(self, i, j, k):
        return _sigma(
            i,
            j,
            k,
            self.index_set_list[i][j],
            self.member_set_list[i][j],
            self.member_set_list_extra[i][j],
            self.basis_vectors,
            self.case,
            self.space_dim,
        )

    def phasor(self, k, n):
        return phasor(k, self.basis_vectors, n, self.space_dim)

    def stiffness_matrix(self, k):
        sigma = bk.zeros((self.dim, self.dim), dtype=bk.complex128)
        for i in range(self.num_nodes):
            for j in range(self.num_nodes):
                sigma[
                    self.n_dof * i : self.n_dof * (i + 1),
                    self.n_dof * j : self.n_dof * (j + 1),
                ] = self._sigma(i, j, k)
        return sigma

    def mass_matrix(self):
        out = bk.zeros((self.num_nodes, self.n_dof), dtype=bk.complex128)
        for i in range(self.num_nodes):
            for j in range(self.n_dof):
                if j >= self.n_dof - 1 and self.case == "frame":
                    out[i, j] = self.moments[i]
                else:
                    out[i, j] = self.masses[i]
        return bk.diag(bk.ravel(out))

    def eigensolve(self, k, vectors=True, tol=1e-6):
        sigma = self.stiffness_matrix(k)
        M = self.mass_matrix()
        if vectors:
            o2, modes = eig(sigma, M, vectors=vectors)
        else:
            o2 = eig(sigma, M, vectors=vectors)
        o2 = bk.where(bk.abs(o2) < tol, 0.0, o2)
        evals = o2.real**0.5
        ievals = bk.argsort(evals)
        if vectors:
            return evals[ievals], modes[:, ievals]
        else:
            return evals[ievals]

    def compute_bands(self, ks, vectors=False):
        eigenvalues = []
        modes = []
        kbar = progbar(ks, "Computing bands", use=self.progress)
        for k in kbar:
            if vectors:
                ev, phi = self.eigensolve(k, vectors=vectors)
                modes.append(phi)
            else:
                ev = self.eigensolve(k, vectors=vectors)
            eigenvalues.append(ev)
        eigenvalues = bk.vstack(eigenvalues)
        if vectors:
            return eigenvalues, bk.stack(modes)
        else:
            return eigenvalues

    def _init_nper(self, nper):
        if isinstance(nper, int):
            if self.space_dim == 1:
                nper = nper, 1
            elif self.space_dim == 2:
                nper = nper, nper, 1
            else:
                nper = nper, nper, nper
        else:
            if len(nper) == self.space_dim == 1 or len(nper) == self.space_dim == 2:
                nper = nper + (1,)
        return nper

    def _init_plot(self, case="static", wbnds=(0.5, 3), mbnds=(6, 12), **kwargs):
        # if case == "static":

        #     cs = [beam.axial_stiffness for beam in self.beams]
        #     unique_bars = []
        # else:
        bars = [m.bar for m in self.members]
        unique_bars = []
        for b in bars:
            if b not in unique_bars:
                unique_bars.append(b)

        cs = [bar.axial_stiffness for bar in unique_bars]

        def _init_bnds(cs, wmin, wmax):
            cmin, cmax = min(cs), max(cs)

            if cmin == cmax:
                rho = bk.ones(len(cs)) * 0.5
            else:
                rho = (bk.array(cs) - cmin) / (cmax - cmin)

            return (wmax - wmin) * rho + wmin

        wplot_beam = _init_bnds(cs, *wbnds)
        wplot_mass = _init_bnds(self.masses, *mbnds)

        colors = ["#ba4545"]  # * len(wplot_mass)

        colors += plt.rcParams["axes.prop_cycle"].by_key()["color"]

        return wplot_mass, wplot_beam, colors, unique_bars

    def plot(self, nper=(1, 1, 1), lc="k", ax=None, alpha=1, **kwargs):
        nper = self._init_nper(nper)
        wplot_mass, wplot_beam, colors, unique_bars = self._init_plot(**kwargs)

        if "colors" in kwargs.keys():
            colors = kwargs["colors"]

        if "wplot_beam" in kwargs.keys():
            wplot_beam = kwargs["wplot_beam"]

        v = self.basis_vectors
        if ax is None:
            if self.space_dim == 3:
                ax = plt.axes(projection="3d")
            else:
                ax = plt.axes()

        for iperx in range(nper[0]):
            for ipery in range(nper[1]):
                for iperz in range(nper[2]):
                    # for ib, b in enumerate(self.beams):
                    for m in self.members:
                        ib = 0
                        for b in unique_bars:
                            if m.bar == b:
                                break
                            ib += 1
                        if self.space_dim == 1:
                            dcoords = iperx * v
                            x0, y0 = m.node0.coordinates + dcoords, 0
                            x1, y1 = m.node1.coordinates + dcoords, 0
                            ax.plot(
                                [x0, x1],
                                [y0, y1],
                                "-",
                                c=lc,
                                lw=wplot_beam[ib],
                                alpha=alpha,
                            )
                        elif self.space_dim == 2:
                            dcoords = iperx * v[0] + ipery * v[1]
                            x0, y0 = m.node0.coordinates + dcoords
                            x1, y1 = m.node1.coordinates + dcoords
                            ax.plot(
                                [x0, x1],
                                [y0, y1],
                                "-",
                                c=lc,
                                lw=wplot_beam[ib],
                                alpha=alpha,
                            )
                        else:
                            dcoords = iperx * v[0] + ipery * v[1] + iperz * v[2]
                            x0, y0, z0 = m.node0.coordinates + dcoords
                            x1, y1, z1 = m.node1.coordinates + dcoords

                            ax.plot3D(
                                [x0, x1],
                                [y0, y1],
                                [z0, z1],
                                "-",
                                c=lc,
                                lw=wplot_beam[ib],
                                alpha=alpha,
                            )

        for iperx in range(nper[0]):
            for ipery in range(nper[1]):
                for iperz in range(nper[2]):
                    dcoords = (
                        iperx * v
                        if self.space_dim == 1
                        else iperx * v[0] + ipery * v[1]
                    )
                    for node in self.nodes:
                        if self.space_dim == 1:
                            dcoords = iperx * v
                            x0, y0 = node.coordinates + dcoords, 0
                            ax.plot(
                                x0,
                                y0,
                                "o",
                                c=colors[node.index],
                                ms=wplot_mass[node.index],
                                alpha=alpha,
                            )
                        elif self.space_dim == 2:
                            dcoords = iperx * v[0] + ipery * v[1]
                            x0, y0 = node.coordinates + dcoords
                            ax.plot(
                                x0,
                                y0,
                                "o",
                                c=colors[node.index],
                                ms=wplot_mass[node.index],
                                alpha=alpha,
                            )

                        else:
                            dcoords = iperx * v[0] + ipery * v[1] + iperz * v[2]
                            x0, y0, z0 = node.coordinates + dcoords
                            ax.scatter3D(
                                x0,
                                y0,
                                z0,
                                c=colors[node.index],
                                s=20 * wplot_mass[node.index],
                                alpha=alpha,
                            )
        if self.space_dim == 3:
            ax.set_box_aspect([1, 1, 1])
        else:
            plt.axis("scaled")
        plt.axis("off")

    def _update(
        self,
        k,
        omega,
        u,
        nper=(1, 1, 1),
        rot_scale=45,
        ax=None,
        xlim=None,
        ylim=None,
        zlim=None,
        **kwargs,
    ):
        nper = self._init_nper(nper)
        wplot_mass, wplot_beam, colors, unique_bars = self._init_plot(
            case="dynamic", **kwargs
        )
        if ax is None:
            if self.space_dim == 3:
                ax = plt.axes(projection="3d")
            else:
                ax = plt.axes()

        if "colors" in kwargs.keys():
            colors = kwargs["colors"]
        nper = self._init_nper(nper)

        v = self.basis_vectors
        N = self.n_dof
        for iperx in range(nper[0]):
            for ipery in range(nper[1]):
                for iperz in range(nper[2]):
                    if self.space_dim == 1:
                        dcoords = iperx * v
                    elif self.space_dim == 2:
                        dcoords = iperx * v[0] + ipery * v[1]
                    else:
                        dcoords = iperx * v[0] + ipery * v[1] + iperz * v[2]
                    for m in self.members:
                        ib = 0
                        for b in unique_bars:
                            if m.bar == b:
                                break
                            ib += 1
                        coords0 = m.node0.coordinates + dcoords
                        coords1 = m.node1.coordinates + dcoords
                        coords = [coords0, coords1]

                        for j, node in enumerate([m.node0, m.node1]):
                            inode = node.index
                            if self.space_dim == 1:
                                cell = bk.array(iperx + node.cell)
                            elif self.space_dim == 2:
                                cell = iperx + node.cell[0], ipery + node.cell[1]
                            else:
                                cell = (
                                    iperx + node.cell[0],
                                    ipery + node.cell[1],
                                    iperz + node.cell[2],
                                )
                            ushift = (u * self.phasor(k, cell)).real
                            du = ushift[inode * N : (inode + 1) * N]
                            if self.case == "frame":
                                du, dtheta = du[:2], du[-1]
                            coords[j] += du

                        if self.space_dim == 1:
                            coords[0] = coords[0], 0
                            coords[1] = coords[1], 0
                        if self.space_dim == 3:
                            ax.plot3D(
                                [coords[0][0], coords[1][0]],
                                [coords[0][1], coords[1][1]],
                                [coords[0][2], coords[1][2]],
                                "-",
                                c="k",
                                lw=wplot_beam[ib],
                            )
                        else:
                            ax.plot(
                                [coords[0][0], coords[1][0]],
                                [coords[0][1], coords[1][1]],
                                "-",
                                c="k",
                                lw=wplot_beam[ib],
                            )

        for iperx in range(nper[0]):
            for ipery in range(nper[1]):
                for iperz in range(nper[2]):
                    if self.space_dim == 1:
                        cell = iperx
                    elif self.space_dim == 2:
                        cell = iperx, ipery
                    else:
                        cell = iperx, ipery, iperz
                    ushift = (u * self.phasor(k, cell)).real
                    for inode, node in enumerate(self.nodes):
                        du = ushift[inode * N : (inode + 1) * N]
                        if self.case == "frame":
                            du, dtheta = du[:2], du[-1]
                            # print(dtheta)
                        if self.space_dim == 1:
                            dcoords = iperx * v[0]
                            x0, y0 = node.coordinates + dcoords + du, 0
                            ax.plot(
                                x0,
                                y0,
                                "o",
                                c=colors[node.index],
                                ms=wplot_mass[node.index],
                            )
                        elif self.space_dim == 2:
                            dcoords = iperx * v[0] + ipery * v[1]
                            x0, y0 = node.coordinates + dcoords + du
                            ax.plot(
                                x0,
                                y0,
                                "o",
                                c=colors[node.index],
                                ms=wplot_mass[node.index],
                            )
                        else:
                            dcoords = iperx * v[0] + ipery * v[1] + iperz * v[2]
                            x0, y0, z0 = node.coordinates + dcoords + du
                            ax.scatter3D(
                                x0,
                                y0,
                                z0,
                                c=colors[node.index],
                                s=20 * wplot_mass[node.index],
                            )
                        if self.case == "frame":
                            l0 = 0.1 * bk.max(
                                bk.linalg.norm(self.basis_vectors, axis=0)
                            )
                            dtheta = dtheta * rot_scale
                            # draw_self_loop(plt.gca(),center=(x0, y0), radius=l0, theta1=0, theta2=dtheta)
                            dt = bk.linspace(0, dtheta, 15)
                            xc, yc = x0 + l0 * bk.cos(dt), y0 + l0 * bk.sin(dt)
                            ax.plot(
                                xc,
                                yc,
                                "-",
                                c="#3867a8",
                                lw=0.75,
                                alpha=0.7,
                            )

        plt.axis("scaled")
        plt.axis("off")
        if self.space_dim == 1:
            plt.title(rf"$k_x$={k:.3f}, $\Omega$={omega:.3f}")
            l0 = bk.linalg.norm(v)
            plt.xlim(-0.2 * l0, (nper[0] + 0.2) * l0)
            plt.xlim(xlim)
            plt.ylim(ylim)
        if self.space_dim == 2:
            plt.title(rf"$k_x$={k[0]:.3f}, $k_y$={k[1]:.3f}, $\Omega$={omega:.3f}")
            ls = [bk.linalg.norm(_) for _ in v]
            plt.xlim(-0.2 * ls[0], (nper[0] + 0.2) * ls[0])
            plt.ylim(-0.2 * ls[1], (nper[1] + 0.2) * ls[1])
            plt.xlim(xlim)
            plt.ylim(ylim)
        else:
            plt.title(
                rf"$k_x$={k[0]:.3f}, $k_y$={k[1]:.3f}, $k_z$={k[2]:.3f}, $\Omega$={omega:.3f}"
            )

            ls = [bk.linalg.norm(_) for _ in v]
            # ax.set_xlim(-0.2 * ls[0], (nper[0]  + 0.2) * ls[0])
            # ax.set_ylim(-0.2 * ls[1], (nper[1]  + 0.2) *  ls[1])
            # ax.set_zlim(-0.2 * ls[2], (nper[2]  + 0.2) *  ls[2])
            ax.set_xlim(xlim)
            ax.set_ylim(ylim)
            ax.set_zlim(zlim)

    def animate(
        self,
        k,
        omega,
        mode,
        ncycle=1,
        nphi=21,
        scale=0.1,
        rot_scale=45,
        nper=(1, 1, 1),
        ax=None,
        filename=None,
        duration=200,
        transparent=False,
        dir_png=None,
        **kwargs,
    ):
        if filename is not None:
            tmpdir = tempfile.mkdtemp()
            fp_in = f"{tmpdir}/animation_tmp_*.png"
        phis = bk.linspace(0, ncycle * 2 * bk.pi, nphi)[:-1]
        for iplot, phi in enumerate(phis):
            u = scale * bk.array(mode, dtype=bk.complex128) * bk.exp(1j * phi)
            if ax is None:
                plt.clf()
            else:
                ax.clear()
            self._update(k, omega, u, nper=nper, rot_scale=rot_scale, ax=ax, **kwargs)
            plt.pause(0.01)
            if filename is not None:
                number_str = str(iplot).zfill(4)
                pngname = f"{tmpdir}/animation_tmp_{number_str}.png"
                fig = plt.gcf()
                # fig.savefig(pngname)
                fig.savefig(pngname, transparent=transparent, facecolor="w", dpi=600)
                # fig.clear()

        if filename is not None:
            img, *imgs = [Image.open(f) for f in sorted(glob.glob(fp_in))]
            img.save(
                fp=filename,
                format="GIF",
                append_images=imgs,
                save_all=True,
                duration=duration,
                loop=0,
            )
            if dir_png is not None:
                os.system(f"mv {tmpdir}/animation_tmp_*.png {dir_png}")
            else:
                os.system(f"rm -f {tmpdir}/animation_tmp_*.png")

    def plot_deform(
        self,
        k,
        omega,
        sol,
        scale=0.1,
        rot_scale=45,
        **kwargs,
    ):
        u = scale * bk.array(sol, dtype=bk.complex128)
        self.plot(alpha=0.2, **kwargs)
        self._update(k, omega, u, rot_scale=rot_scale, **kwargs)
        plt.pause(0.01)


def init_bands(sym_points, nband):
    Gamma_point, M_point, X_point = sym_points
    _kx = bk.linspace(Gamma_point[0], X_point[0], nband)
    _ky = bk.linspace(Gamma_point[1], X_point[1], nband)
    kGammaX = bk.vstack([_kx, _ky])
    _kx = bk.linspace(X_point[0], M_point[0], nband)
    _ky = bk.linspace(X_point[1], M_point[1], nband)
    kXM = bk.vstack([_kx, _ky])
    _kx = bk.linspace(M_point[0], Gamma_point[0], nband)
    _ky = bk.linspace(M_point[1], Gamma_point[1], nband)
    kMGamma = bk.vstack([_kx, _ky])
    ks = bk.vstack([kMGamma[:, :-1].T, kGammaX[:, :-1].T, kXM.T])
    return ks


def init_bands_plot(sym_points, nband):
    Gamma_point, M_point, X_point = sym_points
    dMGamma = bk.linalg.norm(bk.array(Gamma_point) - bk.array(M_point))
    dGammaX = bk.linalg.norm(bk.array(X_point) - bk.array(Gamma_point))
    dXM = bk.linalg.norm(bk.array(M_point) - bk.array(X_point))
    _kx = bk.linspace(0, dMGamma, nband)[:-1]
    _kx1 = dMGamma + bk.linspace(0, dGammaX, nband)[:-1]
    _kx2 = dMGamma + dGammaX + bk.linspace(0, dXM, nband)
    # _ky = bk.linspace(M_point[1], Gamma_point[1], nband)
    # kMGamma = bk.vstack([_kx, _ky])
    ksplot = bk.hstack([_kx, _kx1, _kx2])

    kdist = [dMGamma, dGammaX, dXM]

    return ksplot, kdist


def plot_bands(
    sym_points,
    nband,
    eigenvalues,
    xtickslabels=[r"$M$", r"$\Gamma$", r"$X$", r"$M$"],
    color=None,
    **kwargs,
):
    # nband = int((len(eigenvalues)-2)/3)

    if color == None:
        color = "#4d63c5"
        if "color" in kwargs:
            kwargs.pop("colors")
        if "c" in kwargs:
            kwargs.pop("c")

    ksplot, kdist = init_bands_plot(sym_points, nband)
    plt.plot(ksplot, eigenvalues, color=color, **kwargs)
    # xticks = bk.cumsum(bk.array([0] + kdist))
    xticks = list(accumulate([0] + kdist))
    plt.xticks(xticks, xtickslabels)
    for x in xticks:
        plt.axvline(x, c="#8a8a8a")

    plt.xlim(xticks[0], xticks[-1])

    plt.ylabel(r"$\omega$")


class Truss(Lattice):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, case="truss")


class Frame(Lattice):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, case="frame")


def _sigma_finite(i, j, member_set, member_set1, case):
    s = 0
    for member in member_set:
        _A = _get_A(member, case)
        q = _A[0, 0] * delta(i, j) + _A[0, 1]
        s += q
    for member1 in member_set1:
        _A = _get_A(member1, case)
        q = _A[0, 0] * delta(i, j)
        s += q

    return s


class LatticeFinite(Lattice):
    def __init__(
        self,
        nodes,
        beams,
        case="truss",
        space_dim=2,
        progress=False,
        max_members=None,
        member_indices=None,
    ):
        self.beams = beams
        self.space_dim = space_dim
        self.progress = progress
        self.max_members = max_members
        self.nodes = self._init_nodes(nodes)
        self.members = self._find_members()
        self.case = case
        if space_dim == 1:
            if case == "frame":
                raise ValueError("frame only valid for space_dim>1")
            else:
                self.n_dof = 1
        elif space_dim == 2:
            self.n_dof = 2 if case == "truss" else 3
        elif space_dim == 3:
            raise NotImplementedError("space_dim must be 1 or 2")
        else:
            raise NotImplementedError("space_dim must be 1 or 2")

        self.dim = self.n_dof * self.num_nodes
        self.masses = [s.mass for s in self.nodes]
        self.moments = [s.moment for s in self.nodes]

        # TODO: speedup search for member_set_list
        # self.member_set_list = [
        #     [self.member_set(i, j) for j in range(self.num_nodes)]
        #     for i in range(self.num_nodes)
        # ]
        if member_indices is None:
            self.member_set_indices_list = []
            tnodes = progbar(
                range(self.num_nodes), desc="Finding members indices", use=self.progress
            )
            for i in tnodes:
                _ = [self.member_set_indices(i, j) for j in range(self.num_nodes)]
                self.member_set_indices_list.append(_)
            # self.member_set_indices_list = [
            #     [self.member_set_indices(i, j) for j in range(self.num_nodes)]
            #     for i in range(self.num_nodes)
            # ]
        else:
            self.member_set_indices_list = member_indices
        self.member_set_list = [
            [[self.members[i] for i in p] for p in q]
            for q in self.member_set_indices_list
        ]
        self.member_set_list1 = []
        for i in range(self.num_nodes):
            _ = [self.get_member_set_extra(i, j) for j in range(self.num_nodes)]
            self.member_set_list1.append(_)

        if space_dim == 1:
            self.coords = bk.array([[n.coordinates] for n in self.nodes])
        else:
            self.coords = bk.array([[_c for _c in n.coordinates] for n in self.nodes])

        self.sigma = self.stiffness_matrix()
        self.M = self.mass_matrix()

    @property
    def reciprocal_vectors(self):
        return None

    def _find_members(self):
        tbeams = progbar(self.beams, desc="Finding members", use=self.progress)
        _members = []
        for b in tbeams:
            for node0 in self.nodes:
                if _allclose(node0.coordinates, b.start):
                    break
            for node1 in self.nodes:
                if _allclose(node1.coordinates, b.end):
                    break
            m = Member(node0, node1, b.bar)
            _members.append(m)
            m = Member(node1, node0, b.bar)
            _members.append(m)

        return _members

    def _sigma(self, i, j):
        return _sigma_finite(
            i,
            j,
            self.member_set_list[i][j],
            self.member_set_list1[i][j],
            self.case,
        )

    def stiffness_matrix(self):
        sigma = bk.zeros((self.dim, self.dim), dtype=bk.complex128)
        for i in range(self.num_nodes):
            for j in range(self.num_nodes):
                sigma[
                    self.n_dof * i : self.n_dof * (i + 1),
                    self.n_dof * j : self.n_dof * (j + 1),
                ] = self._sigma(i, j)
        return sigma

    def eigensolve(self, vectors=True, tol=1e-6):
        if vectors:
            o2, modes = eig(self.sigma, self.M, vectors=vectors)
        else:
            o2 = eig(self.sigma, self.M, vectors=vectors)
        o2 = bk.where(bk.abs(o2) < tol, 0.0, o2)
        evals = o2.real**0.5
        ievals = bk.argsort(evals)
        if vectors:
            return evals[ievals], modes[:, ievals]
        else:
            return evals[ievals]

    def solve(self, omega, forces):
        M = self.sigma - omega**2 * self.M

        return bk.linalg.solve(M, forces)

    def plot(self, alpha=1, **kwargs):
        wplot_mass, wplot_beam, colors, unique_bars = self._init_plot(**kwargs)

        if "colors" in kwargs.keys():
            colors = kwargs["colors"]

        # for ib, b in enumerate(self.beams):

        for m in self.members:
            ib = 0
            for b in unique_bars:
                if m.bar == b:
                    break
                ib += 1
            x0, y0 = m.node0.coordinates
            x1, y1 = m.node1.coordinates

            plt.plot([x0, x1], [y0, y1], "-", c="k", lw=wplot_beam[ib], alpha=alpha)

        for node in self.nodes:
            x0, y0 = node.coordinates
            plt.plot(
                x0,
                y0,
                "o",
                c=colors[node.index],
                ms=wplot_mass[node.index],
                alpha=alpha,
            )

            plt.axis("scaled")
            plt.axis("off")

    def _update(
        self,
        omega,
        u,
        rot_scale=45,
        l0=0.03,
        title=False,
        xlim=None,
        ylim=None,
        **kwargs,
    ):
        wplot_mass, wplot_beam, colors, unique_bars = self._init_plot(
            case="dynamic", **kwargs
        )
        if "colors" in kwargs.keys():
            colors = kwargs["colors"]

        N = self.n_dof
        for m in self.members:
            ib = 0
            for b in unique_bars:
                if m.bar == b:
                    break
                ib += 1
            coords0 = copy(m.node0.coordinates)
            coords1 = copy(m.node1.coordinates)
            inode = m.node0.index
            ushift = (u).real
            du = ushift[inode * N : (inode + 1) * N]
            if self.case == "frame":
                du, dtheta = du[:2], du[-1]
            coords0 += du
            inode = m.node1.index
            ushift = (u).real
            du = ushift[inode * N : (inode + 1) * N]
            if self.case == "frame":
                du, dtheta = du[:2], du[-1]
            coords1 += du
            plt.plot(
                [coords0[0], coords1[0]],
                [coords0[1], coords1[1]],
                "-",
                c="k",
                lw=wplot_beam[ib],
            )

        ushift = (u).real
        for inode, node in enumerate(self.nodes):
            inode = node.index
            du = ushift[inode * N : (inode + 1) * N]
            if self.case == "frame":
                du, dtheta = du[:2], du[-1]
                # print(dtheta)
            x0, y0 = node.coordinates + du
            plt.plot(x0, y0, "o", c=colors[node.index], ms=wplot_mass[node.index])

            # print(x0,y0)
            if self.case == "frame":
                # l0 = 0.1 * bk.max(bk.linalg.norm(self.basis_vectors, axis=0))
                # l0 =  0.01*bk.max(self.coords[:,0])
                dtheta = dtheta * rot_scale
                # draw_self_loop(plt.gca(),center=(x0, y0), radius=l0, theta1=0, theta2=dtheta)
                dt = bk.linspace(0, dtheta, 15)
                xc, yc = x0 + l0 * bk.cos(dt), y0 + l0 * bk.sin(dt)
                plt.plot(
                    xc,
                    yc,
                    "-",
                    c="#3867a8",
                    lw=0.75,
                    alpha=0.7,
                )

        plt.axis("scaled")
        plt.axis("off")
        if title:
            plt.title(rf"$\Omega$={omega:.3f}")

        l0 = bk.max(self.coords[:, 0])
        l1 = bk.max(self.coords[:, 1])
        plt.xlim(-0.2 * l0, (1 + 0.2) * l0)
        plt.ylim(-0.2 * l1, (1 + 0.2) * l1)

        plt.xlim(xlim)
        plt.ylim(ylim)
        # plt.tight_layout()

    def plot_deform(
        self,
        omega,
        sol,
        scale=0.1,
        rot_scale=45,
        **kwargs,
    ):
        u = scale * bk.array(sol, dtype=bk.complex128)
        self.plot(alpha=0.2, **kwargs)
        self._update(omega, u, rot_scale=rot_scale, **kwargs)
        plt.pause(0.01)

    def animate(
        self,
        omega,
        sol,
        ncycle=1,
        nphi=21,
        scale=0.1,
        rot_scale=45,
        filename=None,
        duration=200,
        xlim=None,
        ylim=None,
        transparent=False,
        dir_png=None,
        **kwargs,
    ):
        if filename is not None:
            anim = []
            tmpdir = tempfile.mkdtemp()
            fp_in = f"{tmpdir}/animation_tmp_*.png"
        phis = bk.linspace(0, ncycle * 2 * bk.pi, nphi)[:-1]
        for iplot, phi in enumerate(phis):
            u = scale * bk.array(sol, dtype=bk.complex128) * bk.exp(1j * phi)
            plt.clf()
            self._update(omega, u, rot_scale=rot_scale, xlim=xlim, ylim=ylim, **kwargs)
            plt.tight_layout()
            plt.pause(0.01)
            if filename is not None:
                number_str = str(iplot).zfill(4)
                pngname = f"{tmpdir}/animation_tmp_{number_str}.png"
                fig = plt.gcf()
                fig.savefig(pngname, transparent=transparent, facecolor="none", dpi=600)
                fig.clear()

        if filename is not None:
            img, *imgs = [Image.open(f) for f in sorted(glob.glob(fp_in))]
            img.save(
                fp=filename,
                format="GIF",
                append_images=imgs,
                save_all=True,
                duration=duration,
                loop=0,
                transparency=0,
                disposal=2,
            )
            if dir_png is not None:
                os.system(f"mv {tmpdir}/animation_tmp_*.png {dir_png}")
            else:
                os.system(f"rm -f {tmpdir}/animation_tmp_*.png")


class TrussFinite(LatticeFinite):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, case="truss")


class FrameFinite(LatticeFinite):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, case="frame")

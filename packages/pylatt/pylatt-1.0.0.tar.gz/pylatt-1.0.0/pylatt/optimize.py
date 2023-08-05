#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Benjamin Vial
# This file is part of pylatt
# License: GPLv3
# See the documentation at benvial.gitlab.io/pylatt


try:
    import nlopt
except:
    pass
import numpy as npo
from scipy.optimize import differential_evolution
from scipy.optimize import minimize as scipy_minimize

from . import *
from . import backend as bk


def minimize(
    f, x0, bounds, opt_backend="scipy", opt_global=False, options={}, **kwargs
):
    """Minimizer

    Parameters
    ----------
    f : function
        The function to minimize
    x0 : array of length N
        Initial value
    bounds : list of tuples (min,max) of length N
        The bounds for x
    opt_backend : str, optional
        Minimizer backend, either "scipy" or "nlopt", by default "scipy"
    opt_global : bool, optional
        Use scipy's differential evolution algorithm, by default False
    options : dict, optional
        Optins to pass to the minimizer, by default {}

    Returns
    -------
    Object
        An optimization object
    """
    Nvar = len(x0)
    df = grad(f)
    if opt_global:
        opt = differential_evolution(f, bounds, **options)
        x0 = opt.x
    if opt_backend == "scipy":
        opt = scipy_minimize(f, x0, method="L-BFGS-B", jac=df, bounds=bounds, tol=1e-6)
    else:

        def fun_nlopt(x, gradn):
            x = bk.array(x, dtype=bk.float64)
            y = f(x)
            if gradn.size > 0:
                dy = df(x)
                dy = dy.cpu() if (get_backend() == "torch" and DEVICE == "cuda") else dy
                gradn[:] = npo.array(dy, dtype=npo.float64)
            return npo.float64(y)

        opt = nlopt.opt(nlopt.LD_MMA, Nvar)
        lb = npo.array(bounds)[:, 0]
        ub = npo.array(bounds)[:, 1]
        opt.set_lower_bounds(lb)
        opt.set_upper_bounds(ub)
        if "ftol_rel" in options:
            opt.set_ftol_rel(options["ftol_rel"])
        if "xtol_rel" in options:
            opt.set_xtol_rel(options["xtol_rel"])
        if "ftol_abs" in options:
            opt.set_ftol_abs(options["ftol_abs"])
        if "xtol_abs" in options:
            opt.set_xtol_abs(options["xtol_abs"])
        if "stopval" in options:
            opt.set_stopval(options["stopval"])
        if "maxiter" in options:
            opt.set_maxeval(options["maxiter"])
        for k, v in options.items():
            opt.set_param(k, v)
        opt.set_min_objective(fun_nlopt)

        x0 = npo.array(x0)
        opt.x = opt.optimize(x0)
        opt.fun = opt.last_optimum_value()

    return opt

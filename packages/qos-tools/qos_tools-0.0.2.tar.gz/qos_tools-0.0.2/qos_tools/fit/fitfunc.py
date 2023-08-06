# Author: lizhiyuan  <lizhiyuan@baqis.ac.cn>  2021/01/29

import numpy as np
from qos_tools.fit.fitclass import FitClass
from qos_tools.fit import function, plotscript

__all__ = [
    'T1', 'Rabi', 'Ramsey', 'Ramsey_withBeat', 'SpinEcho', 'RB'
]

def T1(data, fixed=None, p0=None, **kw):
    fit = FitClass(data, function._T1, fixed=fixed, p0=p0, **kw)
    fit._plotscript = plotscript.T1
    return fit


def Rabi(data, fixed=None, p0=None, **kw):
    fit = FitClass(data, function._Rabi, fixed=fixed, p0=p0, **kw)
    fit.params['pplen'] = np.abs(0.5/fit.params['Omega'])
    # fit.error['pplen'] = None
    fit._plotscript = plotscript.Rabi
    return fit


def Ramsey(data, fixed=None, p0=None, **kw):
    fit = FitClass(data, function._Ramsey, fixed=fixed, p0=p0, **kw)
    fit.params['Tphi'] = abs(fit.params['Tphi'])
    fit.params['T2star'] = 1/(0.5/fit.params['T1'] + 1/fit.params['Tphi'])
    # fit.error['T2star'] = None
    fit._plotscript = plotscript.Ramsey
    return fit


def Ramsey_withBeat(data, fixed=None, p0=None, **kw):
    fit = FitClass(data, function._Ramsey_withBeat, fixed=fixed, p0=p0, **kw)
    fit.params['Tphi'] = abs(fit.params['Tphi'])
    fit.params['T2star'] = 1/(0.5/fit.params['T1'] + 1/fit.params['Tphi'])
    # fit.error['T2star'] = None
    fit._plotscript = plotscript.Ramsey_withBeat
    return fit


def SpinEcho(data, fixed=None, p0=None, **kw):
    fit = FitClass(data, function._Ramsey, fixed=fixed, p0=p0, **kw)
    fit.params['Tphi'] = abs(fit.params['Tphi'])
    fit.params['T2E'] = 1/(0.5/fit.params['T1'] + 1/fit.params['Tphi'])
    # fit.error['T2E'] = None
    fit._plotscript = plotscript.SpinEcho
    return fit


def RB(data, fixed=None, p0=None, d=2, **kw):
    '''d: d-dimensional system, for the Clifford group, d=2'''
    fit = FitClass(data, function._RB, fixed=fixed, p0=p0, **kw)
    p, p_e = fit.params['p'], fit.error['p']
    fit.params['Fidelity'] = 1-(1-p)*(d-1)/d
    # fit.error['Fidelity'] = p_e*(1-d)/d
    fit._plotscript = plotscript.RB
    return fit

# Author: Liu Pei  <liupei200546@163.com>  2022/03/24

from typing import Optional

import matplotlib.pyplot as plt
import numpy as np
import scipy.linalg as sl
from matplotlib.axes import Axes
from qos_tools.analyzer.tools import get_positive_fft_abs
from scipy.optimize import Bounds, curve_fit, minimize
from sklearn.metrics import r2_score


def _act2msr(sigma: np.ndarray, p1: float = 1, p2: float = 1) -> np.ndarray:
    """
    Add a classical measurement noise to the result of state tomography. 

    Args:
        sigma (np.ndarray): Actual tomography result.
        p1 (float, optional): P(measure = 0|prepare = 0). Defaults to 1.
        p2 (float, optional): P(measure = 1|prepare = 1).. Defaults to 1.

    Returns:
        np.ndarray: Result of measure.
    """
    return (p1+p2-1)*sigma+p1-p2


def _msr2act(sigma: np.ndarray, p1: float = 1, p2: float = 1) -> np.ndarray:
    """
    Calculate the actual result of tomography from a classical measurement noise. 

    Args:
        sigma (np.ndarray): Tomography result.
        p1 (float, optional): P(measure = 0|prepare = 0). Defaults to 1.
        p2 (float, optional): P(measure = 1|prepare = 1). Defaults to 1.

    Returns:
        np.ndarray: Actual result of tomography.
    """
    return (sigma-p1+p2)/(p1+p2-1)


def _sphere2coordinates(x: np.ndarray) -> np.ndarray:
    """
    Transformation from spherical coordinate to rectangular coordinate system.

    Args:
        x (np.ndarray): Spherical coordinate.

    Returns:
        np.ndarray: rectangular coordinate.
    """
    return np.array([x[0]*np.sin(np.pi*x[1])*np.cos(2*np.pi*x[2]), x[0]*np.sin(np.pi*x[1])*np.sin(2*np.pi*x[2]), x[0]*np.cos(np.pi*x[1])])


def _theory_coeff(theta: float, phi: float) -> np.ndarray:
    """
    Coefficient of solution.

    Args:
        theta (float): Oscillation parameter.
        phi (float): Oscillation parameter.

    Returns:
        np.ndarray: Coefficient of evolution curve.
    """

    ox, oy, oz = np.sin(np.pi*theta)*np.cos(2*np.pi*phi), np.sin(np.pi *
                                                                 theta)*np.sin(2*np.pi*phi), np.cos(np.pi*theta)
    con_coeff = np.array([[ox*ox, ox*oy, ox*oz],
                          [oy*ox, oy*oy, oy*oz],
                          [oz*ox, oz*oy, oz*oz]])
    cos_coeff = np.array([[1-ox*ox,   -ox*oy,   -ox*oz],
                          [-oy*ox, 1-oy*oy,   -oy*oz],
                          [-oz*ox,   -oz*oy, 1-oz*oz]])
    sin_coeff = np.array([[0, -oz,  oy],
                          [oz,   0, -ox],
                          [-oy,  ox,   0]])

    return np.array([con_coeff, cos_coeff, sin_coeff])


def _cr_cos_fit(msr: np.ndarray, t: np.ndarray, r2: float = 0.5, ax: Optional[Axes] = None, r: float = 0) -> tuple[float, float]:
    """
    Fitting evolution curve with sinusoidal oscillation.

    Args:
        msr (np.ndarray): Measure result.
        t (np.ndarray): Evolution time.
        r2 (float, optional): R2 of fitting. Defaults to 0.5.
        ax (Optional[Axes], optional): Plot axes. Defaults to None.
        r (float, optional): Oscillation period. Defaults to 0.

    Returns:
        tuple[float, float]: Oscillation parameter theta and phi
    """

    def f_cos(x, a, b, c, d):
        return a*np.cos(2*np.pi*b*x+c)+d

    ret = []
    for i, s in enumerate(msr):
        try:
            popt, pcov = curve_fit(f_cos, t, s, p0=[0.5, r, 0, 0], maxfev=1000000)
            if r2_score(s, f_cos(t, *popt)) > r2:
                ret.append(popt[0])
                if ax is not None:
                    ax.plot(t, f_cos(t, *popt), '--', lw=0.5, ms=2)
            else:
                ret.append((np.max(s)-np.min(s))/2)
        except:
            ret.append((np.max(s)-np.min(s))/2)

    ret = np.asarray(ret)
    sin_theta, tan_phi = np.sqrt(2)*np.abs(ret[2]), np.sqrt(
        np.abs((ret[2]**2+ret[0]**2-ret[1]**2)/(ret[2]**2-ret[0]**2+ret[1]**2)))

    return np.arcsin(sin_theta if sin_theta < 1 else 1), np.arctan(tan_phi)


def theory_evolution(r: float, theta: float, phi: float, sx: float, sy: float, sz: float, p1: float = 1, p2: float = 1, t: Optional[np.ndarray] = None, t0: Optional[float] = None) -> np.ndarray:
    """
    Theoretical evolution curve.

    Args:
        r (float): Oscillation period.
        theta (float): Oscillation parameter.
        phi (float): Oscillation parameter.
        sx (float): Result of tomography of x axis at the initial time.
        sy (float): Result of tomography of y axis at the initial time.
        sz (float): Result of tomography of z axis at the initial time.
        p1 (float, optional): P(measure = 0|prepare = 0). Defaults to 1.
        p2 (float, optional): P(measure = 1|prepare = 1). Defaults to 1.
        t (Optional[np.ndarray], optional): Evolution time. Defaults to None.
        t0 (Optional[float], optional): Initial time. Defaults to None.

    Returns:
        np.ndarray: measure result of theoretical evolution curve.
    """

    coeff = _theory_coeff(theta=theta, phi=phi)
    sigma = _msr2act(np.array([sx, sy, sz]), p1=p1, p2=p2)

    cal = (coeff@sigma).T@np.array([np.ones_like(t),
                                    np.cos(2*np.pi*r*(t-t0)), np.sin(2*np.pi*r*(t-t0))])

    return _act2msr(cal, p1=p1, p2=p2)


def _delta(x: np.ndarray, y: np.ndarray) -> float:
    """
    Calculate the period of evolution.

    Args:
        x (np.ndarray): Time.
        y (np.ndarray): Signal.

    Returns:
        float: Most likely oscillation period.
    """
    freq, amp = get_positive_fft_abs(x, y)
    return float(freq[np.argmax(amp)])


def _minimize_cr(msr: np.ndarray, t: np.ndarray, t0: float, s0: np.ndarray, p1: float = 1, p2: float = 1, random_times: int = 20, r2: float = 0.8, tol: float = 1e-10, ax: Optional[Axes] = None,
                 r2_fit: float = 0.8, fft_pos: int = 2, delta: float = None, **kw) -> tuple[np.ndarray, float]:
    """
    Search evolution parameters.

    Args:
        msr (np.ndarray): Measure result.
        t (np.ndarray): Evolution time.
        t0 (float): Initial time.
        s0 (np.ndarray): Result of tomography at the initial time.
        p1 (float, optional): P(measure = 0|prepare = 0). Defaults to 1.
        p2 (float, optional): P(measure = 1|prepare = 1). Defaults to 1.
        random_times (int, optional): Search times, random evolution parameters are used since the 8th try. Defaults to 20.
        r2 (float, optional): R2 of evolution search. Defaults to 0.8.
        tol (float, optional): Parameters for `minimize` method. Defaults to 1e-10.
        ax (Optional[Axes], optional): Plot axes. Defaults to None.
        r2_fit (float, optional): R2 of fitting. Defaults to 0.8.

    Returns:
        tuple[np.ndarray, float]: Evolution parameters and R2
    """

    def _minimize_cr_eps(x: list, msr: np.ndarray, t: np.ndarray, t0: float):
        return sl.norm(msr-theory_evolution(*x, t, t0))

    _r = _delta(x=t, y=msr[fft_pos]) if delta is None else delta
    _theta, _phi = _cr_cos_fit(msr=msr, t=t, r2=r2_fit, r=_r)

    x0 = [_r, _theta, _phi, *s0, p1, p2]
    random_test = [(i, j) for i in np.arange(0, 1, 0.5)
                   for j in np.arange(0, 1, 0.25)]
    random_test.extend([(np.random.random(), np.random.random())
                       for _ in range(8, random_times)])

    for i, pp in enumerate(random_test):
        x0[1], x0[2] = np.fmod(_theta+pp[0], 1), np.fmod(_phi+pp[1], 1)
        try:
            xx = minimize(_minimize_cr_eps, x0=x0, args=(msr, t, t0), tol=tol,
                        bounds=Bounds((_r*0.8, -0.01, -0.01, -1.01, -1.01, -1.01, 0.49, 0.49),
                                        (_r*1.2,  1.01,  1.01,  1.01,  1.01,  1.01, 1.01, 1.01)))
            fit = theory_evolution(*xx.x, t=t, t0=t0)
            _score = min([r2_score(s, fit[i]) for i, s in enumerate(msr)])
            if _score > r2:
                if ax is not None:
                    ax.plot(t, msr.T, '.', lw=1, ms=2)
                    ax.plot(t, fit.T, '-', lw=1, ms=2)
                return np.array(xx.x[:3]), _score
        except:
            pass
    if ax is not None:
        ax.plot(t, msr.T, '.-', lw=1, ms=2)
    return np.array([np.nan, np.nan, np.nan]), np.nan


def analyzer_cr_tomo_1s(x: np.ndarray, y: np.ndarray, t0_pos: float = 0.5, plot_figure: bool = True, sphere: bool = False, **kw) -> np.ndarray:
    """
    Analyzer for CR Hamiltonian tomography with a single point.

    Args:
        x (np.ndarray): Evolution time.
        y (np.ndarray): Measure data.
        t0_pos (float, optional): Initial time position. Defaults to 0.5.
        plot_figure (bool, optional): Control for plot fitting curve. Defaults to True.

    Returns:
        np.ndarray: CR Coefficient and R2.
    """

    assert y.shape[0] == x.shape[0] and y.shape[1] == 6, 'Invalid data shape.'

    if plot_figure:
        fig, ax = plt.subplots(1, 2, figsize=[9, 2])
    else:
        ax = [None, None]

    t0_cnt = round(x.shape[0]*t0_pos)

    ans0, r2_0 = _minimize_cr(msr=y[:, :3].T, t=x, t0=x[t0_cnt], s0=y[t0_cnt, :3], ax=ax[0], **kw)
    ans1, r2_1 = _minimize_cr(msr=y[:, 3:].T, t=x, t0=x[t0_cnt], s0=y[t0_cnt, 3:], ax=ax[1], **kw)

    if plot_figure:
        plt.tight_layout()
        plt.show()

    if not sphere:
        ans0 = _sphere2coordinates(x=ans0)
        ans1 = _sphere2coordinates(x=ans1)
        ans0, ans1 = (ans0+ans1)/2, (ans0-ans1)/2

    return np.array([*ans0, *ans1, r2_0, r2_1])


def analyzer_cr_tomo_1d(x: np.ndarray, y: np.ndarray, t: np.ndarray, ax: Optional[Axes] = None, with_r2: bool = True, **kw) -> np.ndarray:
    """
    Analyzer for CR Hamiltonian tomography as one parameter changing.

    Args:
        x (np.ndarray): parameters.
        y (np.ndarray): Measure data.
        t (np.ndarray): Evolution time.
        ax (Optional[Axes], optional): Plot axes. Defaults to None.
        with_r2 (bool, optional): Plot R2 data or not. Defaults to True.

    Returns:
        np.ndarray: CR Coefficient and R2.
    """

    if len(t.shape)<2:
        _, tt = np.meshgrid(x, t)
        tt = tt.T
    else:
        tt = t

    y = y.reshape([-1, t.shape[1], 6])
    assert x.shape[0] == y.shape[0], 'Invalid data shape'

    coeff_list = np.array([analyzer_cr_tomo_1s(x=tt[i], y=yy, **kw) for i, yy in enumerate(y)])

    if ax is not None:
        label_list = ['$R_0$', '$\\theta_0$', '$\phi_0$', '$R_1$', '$\\theta_1$', '$\phi_1$'] if kw.get(
            'sphere', False) else ['IX', 'IY', 'IZ', 'ZX', 'ZY', 'ZZ']
        for i in range(6):
            ax.plot(x, coeff_list[:, i], '.-', lw=1, ms=2, label=label_list[i])
        if with_r2:
            ax.plot(x, coeff_list[:, 6], ':', lw=1, ms=2, label='$R^2_0$')
            ax.plot(x, coeff_list[:, 7], ':', lw=1, ms=2, label='$R^2_1$')
        if not kw.get('sphere', False):
            ax.plot(x, np.sqrt(
                coeff_list[:, 0]**2+coeff_list[:, 1]**2), '.--', lw=1, ms=2, label='IXY')
            ax.plot(x, np.sqrt(
                coeff_list[:, 3]**2+coeff_list[:, 4]**2), '.--', lw=1, ms=2, label='ZXY')

    return coeff_list

# Rebulid author: Liu Pei <liupei200546@163.com>  2021/10/10

from typing import Literal, Optional, Union

import numpy as np
from matplotlib.pyplot import Axes
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from scipy.optimize import curve_fit

from qos_tools.analyzer.tools import (get_background_elimination,
                                      get_convolve_arg, get_expsinesquared_arg,
                                      get_interpolation_peaks, get_peaks,
                                      get_positive_fft_abs)
from qos_tools.experiment.lib import generate_RB_cycle
from qos_tools.fit import FitClass, T1, Rabi, Ramsey, Ramsey_withBeat, SpinEcho
from waveforms.math.fit import get_threshold_info
from waveforms.visualization import plotALLXY, plotEllipse

__all__ = [
    'analyzer_S21_abs_min', 'analyzer_S21_abs_min_multiple',
    'analyzer_spectrum',
    'analyzer_Rabi_fit', 'analyzer_Rabi_arg',
    'analyzer_Ramsey', 'analyzer_SpinEcho', 'analyzer_T1',
    'analyzer_Readout2', 'analyzer_Scatter2',
    'analyzer_AllXY', 'analyzer_AllXYtwo',
    'analyzer_RB', 'analyzer_XEB',
    'analyzer_ReadoutDelay', 'analyzer_RTO',
    'check_min', 'check_max', 'analyzer_nop',
]


def plot_population(x, ax: Optional[Axes] = None, population: Optional[np.ndarray] = None):

    if ax is not None and population is not None:
        for ipop in [1, 2, 4]:
            ax.plot(x, population[ipop], '.--', lw=1, ms=2, label=f'{ipop}')
        ax.plot(x, population[0], '--', lw=1, ms=2, label=f'drop')


def analyzer_S21_abs_min(x: np.ndarray, y: np.ndarray,
                         ker: np.ndarray = np.array([0.25, 0.5, 0.25]),
                         alpha: float = 1, ext: str = 'min', interp_points_times: float = 3,
                         ax: Optional[Axes] = None, kind: str = 'cubic', **kw) -> tuple[bool, tuple[float, ...]]:
    """
    Find the frequency according to the min abs of S21. Use `get_convolve_arg`.

    Args:
        x (np.array): frequency.
        y (np.array): S21 amplitude.
        ker (np.ndarray, optional): convolution kernel function. Defaults to np.array([0.25, 0.5, 0.25]).
        alpha (float, optional): the ratio of the difference between extreme value and mean value to standard deviation. Defaults to 1.
        ext (str, optional): extreme value type, maximum, minimum, or both. Defaults to 'min'.
        interp_points_times (float, optional): The ratio of interpolation points to original data points. Defaults to 3.
        ax (Axes, optional): the plot ax. Defaults to None.
        kind (str, optional): interpolation function type, which is used in `numpy.interp1d`. Defaults to 'cubic'.

    Returns:
        tuple[bool, tuple[float, ...]]: flag for success, x corresponding to the minimum y.
    """

    # flag, freq = get_convolve_arg(
    #     x=x, y=y, ker=ker, alpha=alpha, ext=ext, interp_points_times=interp_points_times,
    #     ax=ax, kind=kind)
    flag, freq = get_expsinesquared_arg(
        x=x, y=y, ker=ker, alpha=np.inf, ext=ext, interp_points_times=interp_points_times,
        ax=ax, **kw)

    return flag, (freq,)


def analyzer_S21_abs_min_multiple(x: np.ndarray, y: np.ndarray,
                                  ext: Literal['max', 'min', 'both'] = 'min',
                                  kind: str = 'cubic', interp_points_times: float = 3,
                                  savgol_length_times: Optional[float] = None, savgol_order: int = 1,
                                  height: Optional[float] = None, peak_height_times: float = 0.5,
                                  distance_times: float = 0.1,
                                  ax: Optional[Axes] = None, **kw) -> tuple[bool, tuple[tuple[float, ...], ...]]:
    """
    Find multiple frequencies according to the min abs of S21. Use `get_interpolation_peaks`.

    Args:
        x (np.array): frequency.
        y (np.array): S21 amplitude.
        ker (np.ndarray, optional): convolution kernel function. Defaults to np.array([0.25, 0.5, 0.25]).
        alpha (float, optional): the ratio of the difference between extreme value and mean value to standard deviation. Defaults to 1.
        ext (str, optional): extreme value type, maximum, minimum, or both. Defaults to 'min'.
        interp_points_times (float, optional): The ratio of interpolation points to original data points. Defaults to 3.
        ax (Axes, optional): the plot ax. Defaults to None.
        kind (str, optional): interpolation function type, which is used in `numpy.interp1d`. Defaults to 'cubic'.

    Returns:
        tuple[bool, tuple[float, ...]]: flag for success, x corresponding to the minimum y.
    """

    freq = get_interpolation_peaks(
        x=x, y=y, ext=ext, kind=kind, interp_points_times=interp_points_times,
        savgol_length_times=savgol_length_times, savgol_order=savgol_order, height=height,
        peak_height_times=peak_height_times, distance_times=distance_times, ax=ax)

    return len(freq) > 0, (freq,)


def analyzer_spectrum(x: np.ndarray, y: np.ndarray,
                      ext: Literal['max', 'min', 'both'] = 'max',
                      kind: str = 'cubic', interp_points_times: float = 3,
                      savgol_length_times: Optional[float] = None, savgol_order: int = 1,
                      height: Optional[float] = None, peak_height_times: float = 0.5,
                      distance_times: float = 0.1,
                      ax: Optional[Axes] = None, **kw) -> tuple[bool, tuple[float, ...]]:
    """
    Find spectrum position. Use `get_interpolation_peaks`.

    Args:
        x (np.array): frequency.
        y (np.array): S21 amplitude.
        ker (np.ndarray, optional): convolution kernel function. Defaults to np.array([0.25, 0.5, 0.25]).
        alpha (float, optional): the ratio of the difference between extreme value and mean value to standard deviation. Defaults to 1.
        ext (str, optional): extreme value type, maximum, minimum, or both. Defaults to 'max'.
        interp_points_times (float, optional): The ratio of interpolation points to original data points. Defaults to 3.
        ax (Axes, optional): the plot ax. Defaults to None.
        kind (str, optional): interpolation function type, which is used in `numpy.interp1d`. Defaults to 'cubic'.

    Returns:
        tuple[bool, tuple[float, ...]]: flag for success, x corresponding to the minimum y.
    """

    freq = get_interpolation_peaks(
        x=x, y=y, ext=ext, kind=kind, interp_points_times=interp_points_times,
        savgol_length_times=savgol_length_times, savgol_order=savgol_order, height=height,
        peak_height_times=peak_height_times, distance_times=distance_times, ax=ax)

    return len(freq) > 0, (0 if len(freq) == 0 else freq[-1],)


def analyzer_Rabi_fit(x: np.ndarray, y: np.ndarray,
                      tol: float = 0.8, goal_ans: list[str] = ['pplen', ],
                      height: Optional[float] = None, peak_height_times: float = 0.5,
                      distance_times: float = 0.1,
                      fit_times_tr: Optional[float] = None, fit_phi: float = np.pi,
                      bound_fit: float = 0.2, population: Optional[np.ndarray] = None,
                      ax: Optional[Axes] = None, arg_use: bool = False, **kw) -> Union[FitClass,
                                                                                       tuple[bool, tuple[float, ...]]]:
    """
    Return the pi pulse fitting data, time Rabi or power Rabi, using fitCalss `Rabi`.

    Args:
        x (np.ndarray): time or scale.
        y (np.ndarray): readout signal.
        tol (float, optional): tolerance of fitting goodness. Defaults to 0.8.
        goal_ans (list[str], optional): the target return value of this fit. Defaults to ['pplen', ].
        height (Optional[float], optional): the height in finding peak. Defaults to None.
        peak_height_times (float, optional): ratio of the lowerbound height of a peak to the maximum difference. Defaults to 0.5.
        distance_times (float, optional): ratio of the distance to the number of points between the peaks. Defaults to 0.1.
        fit_times_tr (Optional[float], optional): the initial value of the fitting parameter, with bound (0, np.inf). Defaults to None, i.e. np.inf.
        fit_phi (float, optional): the initial value of the fitting parameter, with bound (-np.pi*2, np.pi*2). Defaults to np.pi.
        bound_fit (float, optional): Fitting parameter boundaries. `A` is (A*(1-bound_fit), A*(1+bound_fit)), `B` is (-A*(2+bound_fit), A*(2+bound_fit)), and `Omega` is (fft_ans*(1-bound_fit), fft_ans*(1+bound_fit)). Defaults to 0.2.
        ax (Optional[Axes], optional): the plot ax. Defaults to None.
        arg_use (bool, optional): whether this fit is used in find arg. Defaults to False.

    Raises:
        ValueError: Searching peaks or maximum value in Rabi analyzer failed.

    Returns:
        Union[FitClass, tuple[bool, tuple[float, ...]]]: return fitclass or flag of success and return ans controlled by `goal_ans`
    """

    ydata = get_background_elimination(y)
    freq, amplitude = get_positive_fft_abs(x, ydata)

    freq_peak_position, _ = get_peaks(
        x=amplitude, height=height, peak_height_times=peak_height_times, distance_times=distance_times)

    p0 = {
        'A': (np.max(y)-np.min(y))/2,
        'B': np.mean(y),
        'phi': fit_phi,
    }

    if len(freq_peak_position) == 0:
        flag, pp = get_convolve_arg(x=freq, y=amplitude, ext='max', alpha=0.1)
        if flag:
            p0['Omega'] = pp
        else:
            raise ValueError(
                f'Searching peaks or maximum value in Rabi analyzer failed.')
    else:
        peak_value, amp = freq[freq_peak_position], amplitude[freq_peak_position]
        peak = np.average(peak_value, weights=amp)
        p0['Omega'] = peak

    l_bound = [p0['A']*(1-bound_fit), -p0['A'] *
               (2+bound_fit), -np.pi*2, p0['Omega']*(1-bound_fit)]
    h_bound = [p0['A']*(1+bound_fit),  p0['A']*(2+bound_fit),
               np.pi*2, p0['Omega']*(1+bound_fit)]

    fixed = {}
    if fit_times_tr is not None:
        p0['Tr'] = fit_times_tr
        l_bound.append(0)
        h_bound.append(np.inf)
    else:
        fixed['Tr'] = np.inf

    bounds = [l_bound, h_bound]

    flag = False
    try:
        RabiFit = Rabi((x, y), fixed=fixed, p0=p0)
        r2 = RabiFit.score()
        flag = r2 > tol
    except:
        pass

    if ax is not None:
        ax.plot(x, y, '.-', lw=1, ms=2)
        if population is not None:
            for ipop in range(population.shape[0]):
                ax.plot(x, population[ipop], '.-', lw=1, ms=2, label=f'{ipop}')
        if flag:
            xNew = np.linspace(np.min(x), np.max(x), 1001)
            ax.plot(xNew, RabiFit.func(xNew), '-',
                    lw=1, ms=2, label=f'$R^2={r2}$')

    if arg_use:
        return None if not flag else RabiFit

    return flag, tuple([0 if not flag else RabiFit.params[goal] for goal in goal_ans])


def analyzer_Rabi_arg(x: np.ndarray, y: np.ndarray,
                      tol: float = 0.8, ax: Optional[Axes] = None,
                      interp_points_times: float = 3, decay_times: float = 0,
                      ext: Literal['max', 'min', 'both'] = 'max',
                      kind: str = 'cubic',
                      savgol_length_times: Optional[float] = None, savgol_order: int = 1,
                      height: Optional[float] = None, peak_height_times: float = 0.5,
                      distance_times: float = 0.1, population: Optional[np.ndarray] = None,
                      alpha_times: float = 0.1, **kw) -> tuple[bool, tuple[float, ...]]:
    """
    Return the pi pulse fitting data, time Rabi or power Rabi, by finding the argmax.

    Args:
        x (np.ndarray): time or scale.
        y (np.ndarray): readout signal.
        tol (float, optional): tolerance of fitting goodness. Defaults to 0.8.
        ax (Optional[Axes], optional): the plot ax. Defaults to None.
        interp_points_times (float, optional): The ratio of interpolation points to original data points. Defaults to 3.
        decay_times (float, optional): a parameter that represents the decay times. The periodic oscillation is multiplied by the previous attenuation to avoid the selection of the second or third period in the multi-period peak search, at the cost of sacrificing some accuracy.a parameters to avoid. Defaults to 0.
        ext (Literal['max', 'min', 'both'], optional): extreme value type, maximum, minimum, or both. Defaults to 'max'.
        kind (str, optional): interpolation function type, which is used in `numpy.interp1d`. Defaults to 'cubic'.
        savgol_times (Optional[float], optional): the parameters for savgol filter. Defaults to None.
        savgol_order (int, optional): the parameters for savgol filter. Defaults to 1.
        height (Optional[float], optional): the height in finding peak. Defaults to None.
        peak_height_times (float, optional): ratio of the lowerbound height of a peak to the maximum difference. Defaults to 0.5.
        distance_times (float, optional): ratio of the distance to the number of points between the peaks. Defaults to 0.1.

    Returns:
        tuple[bool, tuple[float, ...]]: return fitclass or flag of success and pi pulse paramters
    """

    plot_population(x=x, ax=ax, population=population)

    if population is not None:
        y = population[2]-population[1]

    # RabiFit = analyzer_Rabi_fit(x=x, y=y, arg_use=True, tol=tol, ax=ax)

    # if RabiFit is not None:
    #     xNew = np.linspace(np.min(x), np.max(
    #         x), interp_points_times*x.shape[0]+1)
    #     decay_rate = np.exp(-xNew*decay_times/np.max(x))
    #     flag, peak = get_convolve_arg(x=xNew, y=RabiFit.func(
    #         xNew)*decay_rate, ext=ext, alpha=0.2, ax=ax)

    #     return flag, (peak, )

    # decay_rate = np.exp(-x*decay_times/np.max(x))

    # peaks = get_interpolation_peaks(x=x, y=y*decay_rate, ext=ext, kind=kind,
    #                                 interp_points_times=interp_points_times, savgol_length_times=savgol_length_times, savgol_order=savgol_order,
    #                                 height=height, peak_height_times=peak_height_times,
    #                                 distance_times=distance_times, ax=ax)

    # if len(peaks) == 0:
    #     flag, peak = get_convolve_arg(
    #         x, y*decay_rate, ext=ext, ax=ax, alpha=0.1)
    #     if flag:
    #         peaks = [peak]

    flag, peak = get_expsinesquared_arg(
        x=x, y=y, ext=ext, ax=ax, alpha=alpha_times*(np.max(y)-np.min(y)), **kw)
    return flag, (peak, )


def analyzer_Ramsey(x: np.ndarray, y: np.ndarray,
                    tol: float = 0.8, ax: Optional[Axes] = None, goal_ans: list[str] = ['Delta'],
                    height: Optional[float] = None, peak_height_times: float = 0.3,
                    distance_times: float = 0.01,
                    fit_t1: Optional[float] = None, fit_tphi: Optional[float] = None,
                    bound_fit: float = 0.2, fit_delta2: Optional[float] = None,
                    fit_phi: float = 0, fit_phi2: float = np.pi/2, population: Optional[np.ndarray] = None, **kw) -> tuple[bool, tuple[float, ...]]:
    """
    Analyze Ramsey result, using fit class `Ramsey` first or `Ramsey_withBeat` if `Ramsey` failed.

    Args:
        x (np.ndarray): delay time.
        y (np.ndarray): readout signal.
        tol (float, optional): tolerance of fitting goodness. Defaults to 0.8.
        ax (Optional[Axes], optional): the plot ax. Defaults to None.
        goal_ans (list[str], optional): the target return value of this fit. Defaults to ['Delta'].
        height (Optional[float], optional): the height in finding peak. Defaults to None.
        peak_height_times (float, optional): ratio of the lowerbound height of a peak to the maximum difference. Defaults to 0.5.
        distance_times (float, optional): ratio of the distance to the number of points between the peaks. Defaults to 0.01.
        fit_t1 (Optional[float], optional): fitting T1, with bound (0, np.inf). Defaults to None, i.e. np.inf.
        fit_tphi (Optional[float], optional): fitting Tphi, with bound (0, np.inf). Defaults to None, i.e. np.inf.
        bound_fit (float, optional): Fitting parameter boundaries. `A` is (A*(1-bound_fit), A*(1+bound_fit)), `B` is (-A*(2+bound_fit), A*(2+bound_fit)), and `Delta` and `Delta2` is (fft_ans*(1-bound_fit), fft_ans*(1+bound_fit)). Defaults to 0.2.
        fit_delta2 (Optional[float], optional): fitting the second frequency of oscillation. Defaults to none, i.e. try to analyze from fft spectrum.
        fit_phi (float, optional): fitting phi with bound (-2*np.pi, 2*np.pi). This is sensitive in fitting. Defaults to 0.
        fit_phi2 (float, optional): fitting phi2 with bound (-2*np.pi, 2*np.pi). Defaults to np.pi/2.

    Returns:
        tuple[bool, tuple[float, ...]]: flag of success and return ans controlled by `goal_ans`
    """

    plot_population(x=x, ax=ax, population=population)

    ydata = get_background_elimination(y)
    freq, amp = get_positive_fft_abs(x, ydata)
    peak_position, _ = get_peaks(x=amp, height=height, peak_height_times=peak_height_times,
                                 distance_times=distance_times)
    p0 = {
        'A': (np.max(ydata)-np.min(ydata))/2,
        'B': 0,
        'phi': fit_phi,
    }

    l_bound = [p0['A']*(1-bound_fit), -p0['A']*(2+bound_fit), -np.pi*2]
    h_bound = [p0['A']*(1+bound_fit),  p0['A']*(2+bound_fit),  np.pi*2]

    fixed = dict(T1=np.inf if fit_t1 is None else fit_t1)

    if fit_tphi is not None:
        l_bound.append(0)
        h_bound.append(np.inf)
        p0['Tphi'] = fit_tphi
    else:
        fixed['Tphi'] = np.inf

    if ax is not None:
        ax.plot(x, y, '.-', lw=1, ms=2)

    if len(peak_position):

        flag = False
        p0['Delta'] = freq[peak_position[0]]
        l_bound.append(p0['Delta']*(1-bound_fit))
        h_bound.append(p0['Delta']*(1+bound_fit))

        try:
            RamseyFit = Ramsey((x, ydata), fixed=fixed,
                               p0=p0)
            flag = RamseyFit.score() > tol
        except:
            pass

        if flag:
            if ax is not None:
                ax.plot(x, ydata, '.', lw=1, ms=2)
                ax.plot(x, RamseyFit.func(x), '-', lw=1, ms=2)
            return flag, tuple([RamseyFit.params[goal] for goal in goal_ans])
        else:
            if len(peak_position) > 1:
                p0['Delta'] = np.average(
                    freq[peak_position], weights=amp[peak_position])
                p0['Delta2'] = np.abs(
                    freq[peak_position[1]]-freq[peak_position[0]])
            else:
                delta = p0['Delta']
                delta2 = fit_delta2 if fit_delta2 is not None else get_convolve_arg(x=amp[peak_position[0]:],
                                                                                    y=amp[peak_position[0]:], alpha=0.1, ext='max')
                p0['Delta'], p0['Delta2'] = delta+delta2, np.abs(delta-delta2)

            l_bound[-1], h_bound[-1] = p0['Delta'] * \
                (1-bound_fit), p0['Delta']*(1+bound_fit)
            p0['phi2'] = fit_phi2
            l_bound.append(-np.pi*2)
            h_bound.append(np.pi*2)
            l_bound.append(p0['Delta2']*(1-bound_fit))
            h_bound.append(p0['Delta2']*(1+bound_fit))

            try:
                RamseyFit = Ramsey_withBeat(
                    (x, ydata), fixed=fixed, p0=p0)
                flag = RamseyFit.score() > tol
            except:
                pass

            if flag:
                if ax is not None:
                    ax.plot(x, ydata, '.', lw=1, ms=2)
                    ax.plot(x, RamseyFit.func(x), '-', lw=1, ms=2)
                return flag, tuple([RamseyFit.params[goal] for goal in goal_ans])

    return False, (0, )


def analyzer_SpinEcho(x: np.ndarray, y: np.ndarray,
                      tol: float = 0.8, ax: Optional[Axes] = None, goal_ans: list[str] = ['Delta'],
                      height: Optional[float] = None, peak_height_times: float = 0.3,
                      distance_times: float = 0.01,
                      fit_t1: Optional[float] = None, fit_tphi: Optional[float] = None, fit_phi: float = 0,
                      bound_fit: float = 0.2, population: Optional[np.ndarray] = None, **kw) -> tuple[bool, tuple[float, ...]]:
    """
    Analyze spin echo/CP/CPMG result, using fit class `SpinEcho`.

    Args:
        x (np.ndarray): delay time.
        y (np.ndarray): readout signal.
        tol (float, optional): tolerance of fitting goodness. Defaults to 0.8.
        ax (Optional[Axes], optional): the plot ax. Defaults to None.
        goal_ans (list[str], optional): the target return value of this fit. Defaults to ['Delta'].
        height (Optional[float], optional): the height in finding peak. Defaults to None.
        peak_height_times (float, optional): ratio of the lowerbound height of a peak to the maximum difference. Defaults to 0.5.
        distance_times (float, optional): ratio of the distance to the number of points between the peaks. Defaults to 0.01.
        fit_t1 (Optional[float], optional): fitting T1, with bound (0, np.inf). Defaults to None, i.e. np.inf.
        fit_tphi (Optional[float], optional): fitting Tphi, with bound (0, np.inf). Defaults to None, i.e. np.inf.
        bound_fit (float, optional): Fitting parameter boundaries. `A` is (A*(1-bound_fit), A*(1+bound_fit)), `B` is (-A*(2+bound_fit), A*(2+bound_fit)), and `Delta` is (fft_ans*(1-bound_fit), fft_ans*(1+bound_fit)). Defaults to 0.2.
        fit_phi (float, optional): fitting phi with bound (-2*np.pi, 2*np.pi). This is sensitive in fitting. Defaults to 0.

    Returns:
        tuple[bool, tuple[float, ...]]: flag of success and return ans controlled by `goal_ans`
    """

    if population is not None:
        for ipop in range(population.shape[0]):
            ax.plot(x, population[ipop], '.-', lw=1, ms=2, label=f'{ipop}')

    ydata = get_background_elimination(y)
    freq, amp = get_positive_fft_abs(x, ydata)
    peak_position, _ = get_peaks(
        x=amp, height=height, peak_height_times=peak_height_times, distance_times=distance_times)
    p0 = {
        'A': (np.max(ydata)-np.min(ydata))/2,
        'B': 0,
        'phi': fit_phi,
    }

    l_bound = [p0['A']*(1-bound_fit), -p0['A']*(2+bound_fit), -np.pi*2]
    h_bound = [p0['A']*(1+bound_fit),  p0['A']*(2+bound_fit),  np.pi*2]

    fixed = dict(T1=np.inf if fit_t1 is None else fit_t1)

    if fit_tphi is not None:
        l_bound.append(0)
        h_bound.append(np.inf)
        p0['Tphi'] = fit_tphi
    else:
        fixed['Tphi'] = np.inf

    if ax is not None:
        ax.plot(x, y, '.-', lw=1, ms=2)

    if len(peak_position):

        flag = False
        p0['Delta'] = freq[peak_position[0]]
        try:
            SpinEchoFit = SpinEcho(
                (x, ydata), fixed=fixed, p0=p0)
            flag = SpinEchoFit.score() > tol
        except:
            pass

        if flag:
            if ax is not None:
                ax.plot(x, ydata, '.', lw=1, ms=2)
                ax.plot(x, SpinEchoFit.func(x), '-', lw=1, ms=2)

            return flag, tuple([SpinEchoFit.params[goal] for goal in goal_ans])

    return False, (0, )


def analyzer_T1(x: np.ndarray, y: np.ndarray,
                tol: float = 0.8, goal_ans: list[str] = ['T1'], ax: Optional[Axes] = None,
                fit_t1: float = 100e-6, bound_fit: float = 0.2, population: Optional[np.ndarray] = None, **kw) -> tuple[bool, tuple[float, ...]]:
    """
    Analyze T1 result, using fit class `T1`.

    Args:
        x (np.ndarray): wait time.
        y (np.ndarray): readout signal.
        tol (float, optional): tolerance of fitting goodness. Defaults to 0.8.
        goal_ans (list[str], optional): the target return value of this fit. Defaults to ['T1'].
        ax (Optional[Axes], optional): the plot ax. Defaults to None.
        fit_t1 (float, optional): fitting T1, with bound (0, np.inf). Defaults to 100e-6.
        bound_fit (float, optional): fitting parameter boundaries. `A` is (A*(1-bound_fit), A*(1+bound_fit)), `B` is (-A*(1+bound_fit), A*(1+bound_fit)). Defaults to 0.2.

    Returns:
        tuple[bool, tuple[float, ...]]: flag of success and return ans controlled by `goal_ans`.
    """

    if population is not None:
        for ipop in range(population.shape[0]):
            ax.plot(x, population[ipop], '.-', lw=1, ms=2, label=f'{ipop}')

    p0 = {
        'A': np.max(y)-np.min(y),
        'B': np.mean(y),
        'T1': fit_t1,
    }

    l_bound = [-p0['A']*(1+bound_fit), -p0['B']*(1+bound_fit), 0]
    h_bound = [p0['A']*(1+bound_fit),  p0['B']*(1+bound_fit), np.inf]

    if ax is not None:
        ax.plot(x, y, '.-', lw=1, ms=2)

    flag = False
    try:
        T1Fit = T1((x, y), fixed={}, p0=p0)
        flag = T1Fit.score() > tol
    except:
        pass

    if flag:
        if ax is not None:
            ax.plot(x, y, '.', lw=1, ms=2)
            ax.plot(x, T1Fit.func(x), '-', lw=1, ms=2)

        return flag, tuple([T1Fit.params[goal] for goal in goal_ans])

    return False, (0, )


def analyzer_Readout2(x: np.ndarray, S0: np.ndarray, S1: np.ndarray,
                      ax: Optional[Axes] = None, ax1: Optional[Axes] = None,
                      alpha: float = 0.5, beta: float = 0.5,
                      alpha_times: float = 0.1,
                      r: float = 2, **kw) -> tuple[bool, tuple[float, ...]]:
    """
    Analyzer 0 state (ground state) and 1 state (the first excited state) result, using support vector machine.

    Args:
        x (np.ndarray): independent variable array. 
        S0 (np.ndarray): 0 state readout.
        S1 (np.ndarray): 1 state readout.
        ax (Optional[Axes], optional): the main plot ax. Defaults to None.
        ax1 (Optional[Axes], optional): the secondary plot ax. Defaults to None.
        alpha (float, optional): coefficient of distance between two states in the cost function. Defaults to 0.5.
        beta (float, optional): coefficient of visibility between two states in the cost function. Defaults to 0.5.
        r (float, optional): the radius multiple of two ellipses in a scatter plot. Defaults to 2.

    Returns:
        tuple[bool, tuple[float, ...]]: the flag of success and the parameter corresponds to the maximum separate position.
    """

    dis = []
    vis = []
    for i in range(x.shape[0]):
        info = get_threshold_info(S0[i], S1[i])
        dis.append(np.abs(info['center'][0]-info['center'][1]))
        vis.append(info['visibility'][0])
    dis = np.asarray(dis)
    dis = dis/np.max(dis)
    vis = np.asarray(vis)

    cost = alpha*(dis)**2+beta*vis**2

    # flag, arg = get_convolve_arg(
    #     x=range(x.shape[0]), y=cost, ext='max', alpha=0.5)
    flag, arg = get_expsinesquared_arg(interp_points_times=1, x=np.arange(x.shape[0]), y=cost, ext='max', ax=ax, alpha=alpha_times*(np.max(cost)-np.min(cost)), **kw)
    arg = round(arg)
    if ax is not None:
        if flag:
            if ax1 is not None:
                ax1.plot(np.real(S0[arg]), np.imag(
                    S0[arg]), 'C0.', lw=1, ms=2, alpha=0.5)
                ax1.plot(np.real(S1[arg]), np.imag(
                    S1[arg]), 'C1.', lw=1, ms=2, alpha=0.5)
                plotEllipse(c0=info['center'][0], a=r*info['std']
                            [0], b=r*info['std'][1], phi=info['phi'], ax=ax1)
                plotEllipse(c0=info['center'][1], a=r*info['std']
                            [2], b=r*info['std'][3], phi=info['phi'], ax=ax1)

    return flag, (x[arg], )


def analyzer_Scatter2(S0: np.ndarray, S1: np.ndarray,
                      ax: Optional[Axes] = None, tol: float = 0.8,
                      hot_thresh: int = 10000, r: float = 2, **kw) -> tuple[bool, tuple[float, ...]]:
    """
    Analyzer the readout information in 0 and 1 states, using support vector machine.

    Args:
        S0 (np.ndarray): 0 state readout.
        S1 (np.ndarray): 1 state readout.
        ax (Optional[Axes], optional): the plot ax. Defaults to None.
        tol (float, optional): the lower bound of visibility. Defaults to 0.8.
        hot_thresh (int, optional): used in plot process. Defaults to 10000.
        r (float, optional): the radius multiple of two ellipses in a scatter plot. Defaults to 2.

    Returns:
        tuple[bool, tuple[float, ...]]: flag of success and readout info
    """

    info = get_threshold_info(S0, S1)

    if ax is not None:

        ax.set_xticks([])
        ax.set_yticks([])
        for s in ax.spines.values():
            s.set_visible(False)

        re0, re1 = info['signal']

        ax3 = inset_axes(ax, width='65%', height='65%', loc='lower left')

        ax3.hist(re0, bins=50, alpha=0.5)
        ax3.hist(re1, bins=50, alpha=0.5)

        x, a, b, c = info['cdf']
        ax1 = ax3.twinx()
        ax1.plot(x, a)
        ax1.plot(x, b)
        ax1.plot(x, c)
        ax1.set_ylim(0, 1.1)
        ax3.set_title(f"{info['visibility'][0]:.4f}")

        ax2 = inset_axes(ax, width='30%', height='30%', loc='upper right')

        if (len(S0) + len(S1)) < hot_thresh:
            ax2.plot(np.real(S0), np.imag(S0), '.', ms=2, alpha=0.5)
            ax2.plot(np.real(S1), np.imag(S1), '.', ms=2, alpha=0.5)
        else:
            _, *bins = np.histogram2d(np.real(np.hstack([S0, S1])),
                                      np.imag(np.hstack([S0, S1])),
                                      bins=50)

            H0, *_ = np.histogram2d(np.real(S0),
                                    np.imag(S0),
                                    bins=bins,
                                    density=True)
            H1, *_ = np.histogram2d(np.real(S1),
                                    np.imag(S1),
                                    bins=bins,
                                    density=True)
            vlim = max(np.max(np.abs(H0)), np.max(np.abs(H1)))

            ax2.imshow(
                H1.T - H0.T, alpha=(np.fmax(H0.T, H1.T) / vlim).clip(0, 1), interpolation='nearest', origin='lower', cmap='coolwarm', vmin=-vlim,
                vmax=vlim, extent=(bins[0][0], bins[0][-1], bins[1][0], bins[1][-1]))

        for s in ax2.spines.values():
            s.set_visible(False)

        plotEllipse(c0=info['center'][0]*np.exp(1j*info['phi']), a=r*info['std'][0],
                    b=r*info['std'][1], phi=info['phi'], ax=ax2)
        plotEllipse(c0=info['center'][1]*np.exp(1j*info['phi']), a=r*info['std'][2],
                    b=r*info['std'][3], phi=info['phi'], ax=ax2)

        im0, im1 = info['idle']
        lim = min(im0.min(), im1.min()), max(im0.max(), im1.max())
        t = (np.linspace(lim[0], lim[1], 3) + 1j *
             info['threshold']) * np.exp(-1j * info['phi'])
        ax2.plot(t.imag, t.real, 'k--')

        ax2.plot(np.real(info['center'][0]*np.exp(1j*info['phi'])), np.imag(
            info['center'][0]*np.exp(1j*info['phi'])), 'o', color='C3')
        ax2.plot(np.real(info['center'][1]*np.exp(1j*info['phi'])), np.imag(
            info['center'][1]*np.exp(1j*info['phi'])), 'o', color='C4')

        ax2.axis('equal')
        ax2.set_xticks([])
        ax2.set_yticks([])

    return info['visibility'][0] > tol, (info['threshold'], info['phi'])


def analyzer_AllXY(y: np.ndarray,
                   ax: Optional[Axes] = None, tol: float = 0.98, population: Optional[np.ndarray] = None, 
                   ave_goal: Optional[np.ndarray] = None, **kw) -> tuple[bool, tuple[float, ...]]:
    """
    Plot AllXY result and try to analyze it. 'error = sum(std)+sum(|value - goal|)/4.'

    Args:
        y (np.ndarray): AllXY result.
        ax (Optional[Axes], optional): the plot ax. Defaults to None.
        tol (float, optional): the upper bound on the error. Defaults to 0.98.

    Returns:
        tuple[bool, tuple[float, ...]]: flag of success and the error.
    """

    plot_population(x=range(21), ax=ax, population=population)

    pos = [np.arange(0, 5), np.arange(5, 17), np.arange(17, 21)]

    data_std = []
    data_ave = []
    for i, item in enumerate(pos):
        data_std.append(np.std(y[item]))
        data_ave.append(np.mean(y[item]))
    data_ave = np.asarray(data_ave)
    data_std = np.asarray(data_std)
    print(data_ave)
    ave_goal = data_ave if ave_goal is None else ave_goal

    err = np.sum(data_std)+np.sum(np.abs(data_ave-ave_goal))/4

    if ax is not None:
        plotALLXY(y, ax=ax)
        ax.legend(title=f'{err}')

    return err < tol, (err, )


def analyzer_AllXYtwo(x: np.ndarray, y1: np.ndarray, y2: np.ndarray,
                      ax: Optional[Axes] = None,
                      interp_points_times: float = 3, polyfit_order: int = 8, population: Optional[np.ndarray] = None, **kw) -> tuple[bool, tuple[float, ...]]:
    """
    In the DRAG parameters calibration, find the intersection of two terms in AllXY series.

    Args:
        x (np.ndarray): independent variable array.
        y1 (np.ndarray): result of one item in AllXY series.
        y2 (np.ndarray): result of another item in AllXY series.
        ax (Optional[Axes], optional): the plot ax. Defaults to None.
        interp_points_times (float, optional): The ratio of interpolation points to original data points. Defaults to 3.
        polyfit_order (int, optional): use `np.polyfit` to smooth the result, this is the order paramster. Defaults to 8.

    Returns:
        tuple[bool, tuple[float, ...]]: flag of success and the best parameter.
    """

    # plot_population(x=x, ax=ax, population=population)

    fit1 = np.polyfit(x, y1, polyfit_order)
    fit2 = np.polyfit(x, y2, polyfit_order)
    func1 = np.poly1d(fit1)
    func2 = np.poly1d(fit2)

    xx = np.linspace(np.min(x), np.max(x), round(
        interp_points_times*x.shape[0])+1)
    flag = (func1(np.min(x))-func2(np.min(x))) * \
        (func1(np.max(x))-func2(np.max(x))) < 0

    if ax is not None:
        ax.plot(x, y1, '.-', lw=1, ms=2)
        ax.plot(x, y2, '.-', lw=1, ms=2)

        ax.plot(xx, func1(xx), '-', lw=1, ms=2)
        ax.plot(xx, func2(xx), '-', lw=1, ms=2)

        ax.axvline(x=xx[np.argmin(np.abs(func1(xx)-func2(xx)))],
                   c='k', ls='-', lw=1)

    return flag, (xx[np.argmin(np.abs(func1(xx)-func2(xx)))], )


def rb_error(p, pc, d, ave=None, p_ref=None, pc_ref=None):
    if p_ref is None:
        return (1-p)*(1-d)/ave, np.sqrt(pc)*(1-d)/ave
    else:
        return (1-p/p_ref)*(1-d), np.abs(p/p_ref)/2*np.sqrt(pc/p**2+pc_ref/p_ref**2)


def analyzer_RB(y: list[np.ndarray], max_cycle: int, sweep_points: int, random_times: int,
                 interleaves: list[str] = [], ave: float = 1.5, start: int = 1, d = 1/2,
                 ax = None, ref_index: int = 1, tol: float = 0.998, share_base=False, **kw) -> tuple[bool, tuple[float, ...]]:

    def rb_curve(n, p, A, B):
        return A * p**n + B
    
    from scipy.optimize import curve_fit
    from qos_tools.experiment.libs.tools import generate_log_intlist
    x = generate_log_intlist(max_int=max_cycle, sweep_points=sweep_points, min_int=start)
    xx = np.linspace(x.min(), x.max(), 101)

    yy, ee = np.mean(y, axis=1), np.std(y, axis=1)/np.sqrt(random_times)
    
    p = []
    p_cov = []
    if share_base:
        _popt, _pcov = curve_fit(rb_curve, x, yy[-1], sigma=ee[-1], p0=[0.99, 0.5, 0.25], maxfev=100000)
        y_base = _popt[2]
        ax.axhline(y=y_base, c='k', ls='--')
    for i, interleave in enumerate(interleaves):
        if share_base:
            _popt, _pcov = curve_fit(lambda n, p, A, B=y_base: rb_curve(n, p, A, B), 
                                     x, yy[i], sigma=ee[i], p0=[0.99, 0.5], maxfev=100000)
        else:
            _popt, _pcov = curve_fit(rb_curve, x, yy[i], sigma=ee[i], p0=[0.99, 0.5, 0.25], maxfev=100000)
        p.append(_popt)
        p_cov.append(_pcov)
    from qos_tools.analyzer.tools import get_error_output
    
    ret = []
    if ax is not None:
        for i, interleave in enumerate(interleaves):
            for j in range(random_times):
                ax.plot(x, y[i, j, :], f'C{i%10}.', alpha=0.2)
                
        for i in range(len(interleaves)):
            if i<ref_index:
                epg, epg_err, epg_dig = get_error_output(*(rb_error(p=p[i][0], pc=p_cov[i][0][0], d=d, ave=ave)))
            else:
                epg, epg_err, epg_dig = get_error_output(*(rb_error(p=p[i][0], pc=p_cov[i][0][0], d=d, 
                                                                    p_ref=p[0][0], pc_ref=p_cov[0][0][0])))              
            ret.extend([p[i][0], p_cov[i][0][0], epg, epg_err, epg_dig])
            epg_print = 'EPG={x:.%df}({y})' % epg_dig
            if share_base:
                ax.plot(xx, rb_curve(xx, *p[i], y_base), f'C{i%10}-')
            else:
                ax.plot(xx, rb_curve(xx, *p[i]), f'C{i%10}-')
            ax.errorbar(x, yy[i], ee[i], fmt='x', capsize=2, c=f'C{i%10}', label=f'{interleaves[i]}: '+epg_print.format(x=epg, y=epg_err))
    return True, np.asarray(ret).reshape([-1, 5])


def analyzer_XEB(seeds: np.ndarray, cycle: np.ndarray, counts: np.ndarray,
                 ax: Optional[Axes] = None, tol: float = 0.998, population: Optional[np.ndarray] = None, **kw) -> tuple[bool, tuple[float, ...]]:

    # def rb_curve(n, p, A, B=0.25):
    #     return A*p**n+B

    # from waveforms.quantum.xeb import Fxeb2

    # ans = []
    # for i, icycle in enumerate(cycle):
    #     ans.append(Fxeb2(qubits=tuple(select5), cycle=icycle, seeds=ran, counts=count[i, :], shots=1024))
    # ans = np.asarray(ans)

    # if ax is not None:
    #     ax.plot(x, y, '.', label='data', ms=2)

    # p = 0
    # try:
    #     popt, pcov = curve_fit(rb_curve, x, y, p0=[0.99, 0.5, 0.5])
    #     p = popt[0]
    #     if ax is not None:
    #         xx = np.linspace(x.min(), x.max(), 1001)
    #         ax.plot(xx, rb_curve(xx, *popt), '-', label='fit', lw=1, ms=2)
    #         ax.legend(title=f'p={100*(popt[0]):.4f}')
    # except:
    #     pass

    p = 0
    return p > tol, (p, )


def analyzer_ReadoutDelay(x: np.ndarray, y: np.ndarray,
                          ax: Optional[Axes] = None,
                          interp_points_times: float = 10, ker: np.array = np.array([0.1, 0.2, 0.4, 0.2, 0.1]),
                          kind: str = 'cubic', population: Optional[np.ndarray] = None, alpha_times: float = 0.1, **kw) -> tuple[bool, tuple[float, ...]]:
    """
    Find the readout delay for probe line, using `get_convolve_arg`.

    Args:
        x (np.ndarray): delay time.
        y (np.ndarray): readout signal.
        ax (Optional[Axes], optional): the plot ax. Defaults to None.
        interp_points_times (float, optional): The ratio of interpolation points to original data points. Defaults to 10.
        ker (np.array, optional): convolve kernel function. Defaults to np.array([0.1, 0.2, 0.4, 0.2, 0.1]).
        kind (str, optional): interpolation function type, which is used in `numpy.interp1d`. Defaults to 'cubic'.

    Returns:
        tuple[bool, tuple[float, ...]]: [description]
    """

    # flag, delay = get_convolve_arg(
    #     x=x, y=y, ker=ker, ext='max', interp_points_times=interp_points_times, ax=ax, kind=kind)
    flag, delay = get_expsinesquared_arg(x=x, y=y, ext='max', interp_points_times=interp_points_times, ax=ax,
                                         alpha=alpha_times*(np.max(y)-np.min(y)))
    return flag, (delay, )


def check_min(x: np.ndarray, y: np.ndarray,
              ax: Optional[Axes] = None, **kw) -> tuple[bool, tuple[float, ...]]:
    """
    Quick check for min value, x's and y's first dimension is 3 and y[1] is the min.

    Args:
        x (np.array): independent variable.
        y (np.array): dependent variable.
        ax (Optional[Axes], optional): [description]. Defaults to None.

    Returns:
        tuple[bool, tuple[float, ...]]: [description]
    """

    if ax is not None:
        ax.plot(x, y, '.-', lw=1, ms=2)

    assert y.shape[0] == 3, 'check number is valid.'

    return np.all((y[0] >= y[1]) and (y[1] <= y[2])), (0,)


def check_max(x: np.ndarray, y: np.ndarray,
              ax: Optional[Axes] = None, **kw) -> tuple[bool, tuple[float, ...]]:
    """
    Quick check for max value, x's and y's first dimension is 3 and y[1] is the max.

    Args:
        x (np.array): independent variable.
        y (np.array): dependent variable.
        ax (Optional[Axes], optional): [description]. Defaults to None.

    Returns:
        tuple[bool, tuple[float, ...]]: [description]
    """

    if ax is not None:
        ax.plot(x, y, '.-', lw=1, ms=2)

    assert y.shape[0] == 3, 'check number is valid.'

    return np.all((y[0] <= y[1]) and (y[1] >= y[2])), (0,)


def analyzer_RTO(x: np.ndarray, y: np.ndarray,
                 ax: Optional[Axes] = None,
                 tol: float = 0.1e6, population: Optional[np.ndarray] = None, **kw) -> tuple[bool, tuple[float, ...]]:
    """
    Analyze the result of RTO.

    Args:
        x (np.ndarray): delay time.
        y (np.ndarray): x-axis projection and y-axis projection.
        ax (Optional[Axes], optional): the plot ax. Defaults to None.
        tol (float, optional): upper limit of frequency variation. Defaults to 0.1e6.

    Returns:
        tuple[bool, tuple[float, ...]]: flag of success and the frequency change.
    """

    if population is not None:
        for ipop in range(population.shape[0]):
            ax.plot(x, population[ipop], '.--', lw=1, ms=2, label=f'{ipop}')

    assert y.shape[0] == 2*x.shape[0], 'Invalid x and y shape'
    y = y.reshape([x.shape[0], 2])
    IQ = y[:, 0]+1j*y[:, 1]
    diff_IQ = np.diff(IQ)
    angle_IQ = np.unwrap(np.angle(diff_IQ), discont=np.pi)
    accuracy = np.mean(np.diff(angle_IQ))/(x[1]-x[0])/np.pi/2

    if ax is not None:
        ax.plot(y[:, 0]*2-1, y[:, 1]*2-1, '.-', lw=1, ms=2)
        ax.scatter(y[0, 0]*2-1, y[0, 1]*2-1)
        ax.axis('equal')

    return accuracy < tol, (accuracy,)


def analyzer_nop(
        flag: bool = True, ax: Optional[Axes] = None, **kw) -> tuple[bool, tuple[float, ...]]:
    """
    A virtual analyzer for nop scanner.

    Args:
        flag (bool, optional): always return flag. Defaults to True.
        ax (Optional[Axes], optional): the plot ax. Defaults to None.

    Returns:
        tuple[bool, tuple[float, ...]]: flag, (0, )
    """

    return flag, (0, )

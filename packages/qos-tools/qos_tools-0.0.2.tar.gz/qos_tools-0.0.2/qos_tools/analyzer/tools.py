# Author: Liu Pei  <liupei200546@163.com>  2021/08/14

from typing import Literal, Optional

import numpy as np
from matplotlib.pyplot import Axes
from pydantic import BaseModel
from scipy.fft import fft, fftfreq
from scipy.interpolate import interp1d
from scipy.signal import argrelextrema, detrend, find_peaks, savgol_filter
from scipy.stats import multivariate_normal
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import ExpSineSquared, WhiteKernel

__all__ = [
    'get_gauss_kernel', 'get_Gauss_kernel_2D', 'get_rotate_phi',
    'get_convolve_with_interpolate', 'get_convolve_arg', 'get_normalization',
    'get_background_elimination', 'get_positive_fft_abs', 'get_peaks', 'get_interpolation_peaks',
    'get_center_minimize', 'get_center_kmeans',
    'get_general_fit', 'get_expsinesquared_arg',
]


class LiteralCheck(BaseModel):
    xy: Optional[Literal['X', 'Y', 'XY']] = None
    ext: Optional[Literal['max', 'min', 'both']] = None
    mode: Optional[Literal['linear', 'constant', 'savgol']] = None


def get_general_fit(x: np.ndarray, y: np.ndarray,
                    length_scale: Optional[float] = None, periodicity: Optional[float] = None,
                    length_scale_bounds: Optional[tuple[float]] = None, periodicity_bounds: Optional[tuple[float]] = None, periodicity_count: int = 1,
                    noise_level: float = 1, noise_level_bounds: tuple[float] = (1e-5, 1e5),
                    interp_points_times: float = 5, ax: Optional[Axes] = None, **kw
                    ) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """ Author Ziyu Tao

    A general smooth method with white noise, use sklearn method.

    Args:
        x (np.ndarray): 1D array, independent variables.
        y (np.ndarray): 1D array, dependent variables.
        length_scale (Optional[float], optional): ExpSineSquared parameters. Defaults to None.
        periodicity (Optional[float], optional): ExpSineSquared parameters. Defaults to None.
        length_scale_bounds (Optional[tuple[float]], optional): ExpSineSquared parameters. Defaults to None.
        periodicity_bounds (Optional[tuple[float]], optional): ExpSineSquared parameters. Defaults to None.
        periodicity_count (int, optional): how much periods in your data. Defaults to 1.
        noise_level (float, optional): WhiteKernel parameters. Defaults to 1.
        noise_level_bounds (tuple[float], optional): WhiteKernel parameters. Defaults to (1e-5, 1e5).
        interp_points_times (float, optional): The ratio of interpolation points to original data points. Defaults to 5.
        ax (Optional[Axes], optional): the plot ax. Defaults to None.

    Returns:
        tuple[np.ndarray, np.ndarray, np.ndarray]: x data and y data after smooth with std 
    """

    length_scale = 1 if length_scale is None else length_scale
    length_scale_bounds = (
        1e-5, 1e5) if length_scale_bounds is None else length_scale_bounds
    periodicity = (np.max(x)-np.min(x)) / \
        periodicity_count if periodicity is None else periodicity
    periodicity_bounds = (
        1e-2*periodicity, 1e2*periodicity) if periodicity_bounds is None else periodicity_bounds

    gp_kernel = ExpSineSquared(length_scale=length_scale, periodicity=periodicity, length_scale_bounds=length_scale_bounds,
                               periodicity_bounds=periodicity_bounds)+WhiteKernel(noise_level=noise_level, noise_level_bounds=noise_level_bounds)

    gpr = GaussianProcessRegressor(kernel=gp_kernel)
    gpr.fit(x.reshape(-1, 1), y.reshape(-1, 1))
    xNew = np.linspace(np.min(np.real(x)), np.max(np.real(x)),
                       round(interp_points_times*x.shape[0])+1)
    yNew, yStd = gpr.predict(xNew.reshape(-1, 1), return_std=True)
    yNew = yNew.reshape([yNew.shape[0], ])
    yStd = yStd.reshape([yStd.shape[0], ])

    if ax is not None:
        ax.fill_between(xNew, yNew-yStd, yNew+yStd, alpha=0.2)
        ax.plot(x, y, '.', lw=1, ms=2)
        ax.plot(xNew, yNew, '-', lw=1, ms=2)

    return xNew, yNew, yStd


def get_expsinesquared_arg(x: np.ndarray, y: np.ndarray,
                           ext: Literal['max', 'min', 'both'] = 'min',
                           ax: Optional[Axes] = None, alpha: float = 0.1, **kw) -> tuple[bool, float]:
    """[summary]

    Args:
        x (np.ndarray): 1D array, independent variables.
        y (np.ndarray): 1D array, dependent variables.
        ext (Literal['max', 'min', 'both'], optional): extreme value type, maximum, minimum, or both. Defaults to 'min'.
        ax (Optional[Axes], optional): the plot ax. Defaults to None.
        alpha (float, optional): std upper bound. Defaults to 0.1.

    Returns:
        tuple[bool, float]: the flag of extreme greater than several times of the standard deviation and the extreme position.
    """

    ext = LiteralCheck(ext=ext).ext
    xNew, yNew, yStd = get_general_fit(x=x, y=y, ax=ax, **kw)

    x_min_pos, = (np.array([], dtype=np.int64),
                  ) if ext == 'max' else argrelextrema(yNew, np.less)
    x_max_pos, = (np.array([], dtype=np.int64),
                  ) if ext == 'min' else argrelextrema(-yNew, np.less)
    x_ans = np.concatenate((x_min_pos, x_max_pos))

    if len(x_ans) == 0:
        x_ans = np.array([yNew.shape[0]//2], dtype=np.int64)

    if ax is not None:
        ax.axvline(x=xNew[x_ans[0]], lw=1, ls='-')

    return yStd[x_ans[0]] < alpha, xNew[x_ans[0]]


def get_error_output(data: float, err: float) -> tuple[float, int, int]:
    """
    Error analysis

    Args:
        data (float): data
        err (float): error

    Returns:
        tuple[float, int, int]: data, err, significant digits
    """

    ret = 0
    if np.isnan(err) or err>1:
        return data, 0, 0
    while round(err) < 1:
        ret += 1
        err = err*10
    return round(data*(10**ret))/10**ret, round(err), ret


def get_center_minimize(S: np.ndarray, N: int) -> np.ndarray:
    """
    Using a simple nearest method to determin centers of clusters on IQ plane.

    Args:
        S (np.ndarray): data, in the shape [n, shots], n is number of groups initially classified and shots is the all data, here all the data n*shots are used in classification algorithm.
        N (int): number of clusters

    Returns:
        np.ndarray: array of centers in complex
    """

    def get_center(x, S, N):
        minS = np.ones([S.shape[0], N])
        for i in range(N):
            minS[:, i] = np.real(np.abs(S-x[i]-1j*x[i+N]))
        minS = np.min(minS, axis=1)
        return np.sum(minS)

    from scipy.optimize import minimize

    x0 = []

    for i in range(N):
        x0.append(np.real(np.mean(S[i])))
    for i in range(N):
        x0.append(np.imag(np.mean(S[i])))

    result = minimize(get_center, x0=x0, args=(S.flatten(), N))

    cList = []
    for i in range(N):
        cList.append(result.x[i]+1j*result.x[i+N])
    cList = np.asarray(cList)
    return cList


def get_center_kmeans(S: np.ndarray, N: int):
    """
    Using kmeans method to determin centers of clusters on IQ plane.

    Args:
        S (np.ndarray): data, in the shape [n, shots], n is number of groups initially classified and shots is the all data, here all the data n*shots are used in classification algorithm.
        N (int): number of clusters

    Returns:
        np.ndarray: array of centers in complex
    """

    def exchange(x, center):
        from itertools import permutations
        assert x.shape[0] == center.shape[0], 'n not equal'
        permutation = list(permutations(range(x.shape[0]), x.shape[0]))
        cost = np.array([np.sum(np.abs(x-center[list(item)])**2)
                        for item in permutation])
        return center[list(permutation[np.argmin(cost)])]

    from sklearn.cluster import KMeans

    SS = S.flatten()
    classification = KMeans(n_clusters=N).fit_predict(
        np.array([np.real(SS), np.imag(SS)]).T)

    clist = []
    for i in range(N):
        clist.append(np.mean(SS[np.where(classification == i)]))
    return exchange(np.array([np.mean(S[i]) for i in range(N)]), np.asarray(clist))


def get_gauss_kernel(halfsize: int = 1, a: float = 2) -> np.ndarray:
    """
    Return the one-dimensional Gaussian convolution kernel function.

    Args:
        halfsize (int, optional): half side of th kernel function and total length is 2*halfsize+1. Defaults to 1.
        a (float, optional): the ratio of the range of values of the Gaussian distribution function to the variance. Defaults to 2.

    Returns:
        np.ndarray: 1D Gaussian convolution kernel function
    """

    rv = multivariate_normal(0, 1)
    x0 = np.linspace(-a, a, 2*halfsize+1)
    _m = rv.pdf(x0)
    m = _m/np.sum(_m)
    return m


def get_Gauss_kernel_2D(halfsize: int = 2, a: float = 2, factor: float = 1,
                        xy: Literal['X', 'Y'] = 'X') -> np.ndarray:
    """
    Return the two-dimensional Gaussian convolution kernel matrix.

    Args:
        halfsize (int, optional): half side of th kernel function and total length is 2*halfsize+1. Defaults to 1.
        a (float, optional): the ratio of the range of values of the Gaussian distribution function to the variance. Defaults to 2.
        factor (float, optional): covariance factor of a two-dimensional Gaussian function. Defaults to 1.
        xy (Literal, optional): control covariance coefficient pattern. Defaults to 'X'.
    Returns:
        np.ndarray: 2D Gaussian convolution kernel matrix。
    """

    xy = LiteralCheck(xy=xy).xy

    mean = [0, 0]
    if xy == 'X':
        cov = [[1, 0], [0, factor]]
    elif xy == 'Y':
        cov = [[factor, 0], [0, 1]]
    else:
        cov = [[1, 0], [0, 1]]
    rv = multivariate_normal(mean, cov)
    x0 = np.linspace(-a, a, 2*halfsize+1)
    x, y = np.meshgrid(x0, x0)
    pos = np.dstack((x, y))
    _m = rv.pdf(pos)
    m = _m/np.sum(_m)
    return m


def get_rotate_phi(x: np.ndarray,
                   ax: Optional[Axes] = None) -> np.ndarray:
    """
    Rotate points on a straight line in the plane onto the X-axis. The point near the origin is going to be on the left.

    Args:
        x (Optional[np.ndarray]): complex data
        ax (Optional[Axes], optional): the plot ax. Defaults to None.

    Returns:
        np.ndarray: the complex data after processed.
    """

    xx = np.ndarray.flatten(x)

    func = np.poly1d(np.polyfit(x=np.real(xx), y=np.imag(xx), deg=1))

    if ax is not None:
        ax.plot(np.real(x), np.imag(x), '.', lw=1, ms=2)
        xNew = np.linspace(np.min(np.real(x)), np.max(np.real(x)), 1001)
        ax.plot(np.real(xNew), func(np.real(xNew)), '-', lw=1, ms=2)

    xmin, xmax = np.argmin(np.real(xx)), np.argmax(np.real(xx))
    slope = (func(np.max(np.real(xx)))-func(np.min(np.real(xx)))) / \
        (np.max(np.real(xx))-np.min(np.real(xx)))

    if np.abs(xx[xmin]) > np.abs(xx[xmax]):
        slope *= -1

    if ax is not None:
        xxx = np.real(x*(1-1j*slope)/np.sqrt(1+slope**2))
        ax.plot(np.real(xxx), np.imag(xxx), '.', lw=1, ms=2)
        ax.plot(np.real(xxx[0]), np.imag(xxx[0]), '.', lw=1, ms=5)

    return np.real(x*(1-1j*slope)/np.sqrt(1+slope**2))


def get_convolve_with_interpolate(x: np.ndarray, y: np.ndarray,
                                  ker: np.ndarray = np.array(
                                      [0.25, 0.5, 0.25]),
                                  interp_points_times: float = 3, kind: str = 'cubic',
                                  ax: Optional[Axes] = None) -> tuple[np.ndarray, np.ndarray]:
    """
    Return y's convolve with interpolation, that is, interpolate the result of the convolution.

    Args:
        x (np.ndarray): ndarray of independent variables.
        y (np.ndarray): ndarray of dependent variables.
        ker (np.ndarray, optional): convolution kernel function. Defaults to np.array([0.25, 0.5, 0.25]).
        interp_points_times (float, optional): The ratio of interpolation points to original data points. Defaults to 3.
        kind (str, optional): interpolation function type, which is used in `numpy.interp1d`. Defaults to 'cubic'.
        ax (Optional[Axes], optional): the plot ax. Defaults to None.

    Returns:
        tuple[np.ndarray, np.ndarray]: x and y after processed.
    """

    convolve_y = np.convolve(y, ker, mode='valid')
    x_offset = (ker.shape[0])//2
    xx = x[x_offset:x_offset+convolve_y.shape[0]]
    func = interp1d(xx, convolve_y, kind=kind)
    xNew = np.linspace(np.min(xx), np.max(xx), round(
        convolve_y.shape[0]*interp_points_times)+1)
    yNew = func(xNew)

    if ax is not None:
        ax.plot(x, y, '.', lw=1, ms=2)
        ax.plot(xNew, yNew, '-', lw=1, ms=2)

    return xNew, yNew


def get_convolve_arg(x: np.ndarray, y: np.ndarray,
                     ker: np.ndarray = np.array([0.25, 0.5, 0.25]),
                     alpha: float = 1, ext: Literal['max', 'min', 'both'] = 'min',
                     interp_points_times: float = 3,
                     ax: Optional[Axes] = None, kind: str = 'cubic') -> tuple[bool, float]:
    """
    Find argmin of argmax of y after a simple convolve with interpolate and return the corresponding item in independent variables

    Args:
        x (np.ndarray): ndarray of independent variables.
        y (np.ndarray): ndarray of dependent variables.
        ker (np.ndarray, optional): convolution kernel function. Defaults to np.array([0.25, 0.5, 0.25]).
        alpha (float, optional): the ratio of the difference between extreme value and mean value to standard deviation. Defaults to 1.
        ext (Literal['max', 'min', 'both'], optional): extreme value type, maximum, minimum, or both. Defaults to 'min'.
        interp_points_times (float, optional): The ratio of interpolation points to original data points. Defaults to 3.
        ax (Axes, optional): the plot ax. Defaults to None.
        kind (str, optional): interpolation function type, which is used in `numpy.interp1d`. Defaults to 'cubic'.

    Returns:
        tuple[bool, float]: the flag of extreme greater than several times of the standard deviation and the extreme position.
    """

    ext = LiteralCheck(ext=ext).ext

    xNew, yNew = get_convolve_with_interpolate(
        x=x, y=y, ker=ker, interp_points_times=interp_points_times, kind=kind, ax=ax)
    std_y = np.std(yNew)

    pos_x, dif_y = (xNew[np.argmax(yNew)], np.abs(np.max(yNew)-np.mean(yNew))) if ext in [
        'max'] else (xNew[np.argmin(yNew)], np.abs(np.min(yNew)-np.mean(yNew)))

    if ax is not None:
        ax.axvline(x=pos_x, lw=1, ls='-')

    return dif_y > std_y*alpha, pos_x


def get_normalization(x: np.ndarray) -> np.ndarray:
    """
    Normalize a array to [0, 1].

    Args:
        x (np.ndarray): a array.

    Returns:
        np.ndarray: the processed array
    """
    return (x-np.min(x))/(1 if np.max(x) == np.min(x) else (np.max(x)-np.min(x)))


def get_background_elimination(x: np.ndarray,
                               mode: Literal['linear',
                                             'constant', 'savgol'] = 'linear',
                               savgol_times: Optional[float] = None, savgol_order: int = 1) -> np.ndarray:
    """
    Return data removed the background of 1D data array.

    Args:
        y (np.ndarray): the data.
        mode (str, optional): in ['linear'(for deducting linear trend), 'constant'(for deducting a constant), 'savgol'(for savgol filter)]. Defaults to 'savgol'.
        savgol_times (Optional[float], optional): the parameters for savgol filter. Defaults to 0.9.
        savgol_order (int, optional): the parameters for savgol filter. Defaults to 1.

    Returns:
        np.ndarray: data after deducting the background
    """

    mode = LiteralCheck(mode=mode).mode

    if mode in ['linear', 'constant']:
        return detrend(x, type=mode)
    else:
        assert savgol_times is not None, 'Please input `savgol_times`.'
        return x-savgol_filter(x, window_length=round(x.shape[0]*savgol_times//2)*2+1, polyorder=savgol_order)


def get_positive_fft_abs(x: np.ndarray, y: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """
    Return the positive frequency of fft.

    Args:
        x (np.array): ndarray of independent variables.
        y (np.array): ndarray of dependent variables.

    Raises:
        ValueError: shape error.

    Returns:
        tuple[np.array, np.array]: fft frequency, fft amplitude.
    """

    if x.shape[0] != y.shape[0] or x.shape[0] == 0 or y.shape[0] == 0:
        raise ValueError('x, y must have the same length or someone is null')
    return fftfreq(x.shape[0], x[1]-x[0])[1:(x.shape[0]//2)], (get_normalization(np.abs(fft(y))))[1:(x.shape[0]//2)]


def get_peaks(x: np.ndarray,
              height: Optional[float] = None, peak_height_times: float = 0.5,
              distance_times: float = 0.1) -> tuple[np.ndarray, dict]:
    """
    Return peaks position.

    Args:
        x (np.ndarray): ndarray of independent variables.
        height (Optional[float], optional): the height in finding peak. Defaults to None.
        peak_height_times (float, optional): ratio of the lowerbound height of a peak to the maximum difference. Defaults to 0.5.
        distance_times (float, optional): ratio of the distance to the number of points between the peaks. Defaults to 0.1.

    Returns:
        tuple[np.ndarray, dict]: [description]
    """

    return find_peaks(x,
                      height=(np.max(x)-np.min(x)) *
                      peak_height_times if height is None else height,
                      distance=max(1, round(distance_times*x.shape[0])))


def get_interpolation_peaks(x: np.ndarray, y: np.ndarray,
                            ext: Literal['max', 'min', 'both'] = 'max',
                            kind: str = 'cubic', interp_points_times: float = 3,
                            savgol_length_times: Optional[float] = None, savgol_order: int = 1,
                            height: Optional[float] = None, peak_height_times: float = 0.5,
                            distance_times: float = 0.1, ax: Optional[Axes] = None) -> list[float]:
    """
    Return peaks after a simple interpolation and background removed, which a savgol filter can be used or not.

    Args:
        x (np.ndarray): ndarray of independent variables.
        y (np.ndarray): ndarray of dependent variables.
        ext (Literal['max', 'min', 'both'], optional): extreme value type, maximum, minimum, or both. Defaults to 'max'.
        kind (str, optional): interpolation function type, which is used in `numpy.interp1d`. Defaults to 'cubic'.
        interp_points_times (float, optional): The ratio of interpolation points to original data points. Defaults to 3.
        height (Optional[float], optional): the height in finding peak. Defaults to None.
        peak_height_times (float, optional): ratio of the lowerbound height of a peak to the maximum difference. Defaults to 0.5.
        distance_times (float, optional): ratio of the distance to the number of points between the peaks. Defaults to 0.1.
        ax (Optional[Axes], optional): the plot ax. Defaults to None.
        savgol_times (Optional[float], optional): the parameters for savgol filter. Defaults to None.
        savgol_order (int, optional): the parameters for savgol filter. Defaults to 1.

    Returns:
        list[float]: the corresponding value of the peaks position.
    """

    ext = LiteralCheck(ext=ext).ext

    ydata = get_background_elimination(y, mode='linear')
    if ext in ['min']:
        ydata = -ydata
    elif ext in ['both']:
        ydata = np.abs(ydata)

    func = interp1d(x, ydata, kind=kind)
    xdata = np.linspace(np.min(x), np.max(
        x), interp_points_times*ydata.shape[0]+1)
    ydata = func(xdata) if savgol_length_times is None else savgol_filter(func(xdata),
                                                                          window_length=int(savgol_length_times*len(xdata)/2)*2+1, polyorder=savgol_order)
    peak_position, _ = get_peaks(
        x=ydata, height=height, peak_height_times=peak_height_times, distance_times=distance_times)

    if ax is not None:
        ax.plot(x, y, '.-', lw=1, ms=2)
        ax.plot(xdata, ydata, '.-', lw=1, ms=2)
        if len(peak_position) > 0:
            for item in xdata[peak_position]:
                ax.axvline(x=item, lw=1, ls='-')
    return xdata[peak_position]


def get_gauss_fit(x: np.ndarray, ax: Optional[Axes] = None, sigma=3, fit=True, **kw):
    def _erf(x, mu, sigma):
        from scipy.special import erf
        return 0.5+0.5*erf(((x-mu)/sigma)/np.sqrt(2))

    from scipy.optimize import curve_fit
    xx, yy = np.sort(x), (np.arange(x.shape[0])+1)/x.shape[0]
    if not fit:
        popt, pcov = np.median(xx), np.std(xx)
        if ax is not None:
            ax.plot(xx, yy, '.-', **kw)
            ax.axvline(x=popt, c=kw.get('c', None))
    else:
        popt, pcov = curve_fit(_erf, xx, yy, p0=[np.mean(x), np.std(x)])
        if ax is not None:
            ax.plot(xx, yy, '.', **kw)
            xxx = np.linspace(popt[0]-popt[1]*sigma, popt[0]+popt[1]*sigma, 1001)
            if 'label' in kw:
                kw.pop('label')
            ax.plot(xxx, _erf(xxx, *popt), '-', **kw)
    
    return popt, pcov

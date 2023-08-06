# Author: Liu Pei  <liupei200546@163.com>  2022/03/10

from typing import Optional

import numpy as np
from matplotlib.axes import Axes
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import (RBF, ConstantKernel,
                                              ExpSineSquared, WhiteKernel)


def plot_gpr(x: np.ndarray,
             y: np.ndarray,
             gpr: GaussianProcessRegressor,
             x_new: Optional[np.ndarray] = None,
             y_new: Optional[np.ndarray] = None,
             y_std: Optional[np.ndarray] = None,
             interp_points_times: float = 10,
             lw: float = 1,
             ms: float = 2,
             ax: Optional[Axes] = None,
             **kw) -> None:

    if x_new is None or y_new is None or y_std is None:
        x_new = np.linspace(np.min(np.real(x)), np.max(np.real(x)),
                            round(interp_points_times * x.shape[0]) + 1)
        y_new, y_std = gpr.predict(x_new.reshape(-1, 1), return_std=True)
        y_new, y_std = y_new.reshape([
            y_new.shape[0],
        ]), y_std.reshape([
            y_std.shape[0],
        ])

    if ax is not None:
        ax.fill_between(x_new, y_new - y_std, y_new + y_std, alpha=0.2)
        ax.plot(x, y, '.', lw=lw, ms=ms)
        ax.plot(x_new, y_new, '-', lw=lw, ms=ms)


def preprocess_1d(x: np.ndarray,
                  mode: str = 'MinMaxScaler',
                  **kw) -> np.ndarray:
    """
    Preprocess for 1d array scaler. `sklearn.preprocessing` are used here.
    Support mode: 'MinMaxScaler', 'MaxAbsScaler', 'RobustScaler', 'StandardScaler'

    Args:
        y (np.ndarray): 1d array.
        mode (str, optional): `sklearn.preprocessing` calss name. Defaults to 'MinMaxScaler'.

    Returns:
        _type_: _description_
    """

    import sklearn.preprocessing as preprocess_lib
    return getattr(preprocess_lib,
                   mode)(**kw).fit_transform(X=x.reshape([-1, 1]))[:, 0]


def exp_sin_kernel(x: np.ndarray, y: np.ndarray,
                   **kw) -> tuple[GaussianProcessRegressor, float]:
    fit_kernel = ConstantKernel()*ExpSineSquared()*RBF() + \
        ConstantKernel()+WhiteKernel()
    gpr = GaussianProcessRegressor(kernel=fit_kernel,
                                   normalize_y=kw.get('normalize_y', False))
    return gpr.fit(x.reshape(-1, 1), y.reshape(-1, 1)+5e-5), 1/gpr.kernel_.get_params()['k1__k1__k1__k2__periodicity']

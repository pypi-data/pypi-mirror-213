# Author: Liu Pei  <liupei200546@163.com>  2021/08/14

from typing import Literal, Optional

import numpy as np


__all__ = [
    'get_SSE', 'get_MSE', 'get_RMSE', 'get_SSR', 'get_SST', 'get_R2',
]


def get_SSE(y: np.ndarray, y_fit: np.ndarray, weights: Optional[np.ndarray] = None) -> float:
    """
    Return sum of squares for residuals (SSE) of y and y_fit, $\sum (y-y_fit)**2$

    Args:
        y (np.array): real data
        y_fit (np.array): estimation or fitting of data
        weights (Optional[np.array], optional): the weights of data. Defaults to None.

    Returns:
        np.float64: sum of squares for residuals(SSE)
    """

    if weights is None:
        weights = np.ones_like(y)
    return np.sum((y-y_fit)**2*weights)


def get_MSE(y: np.ndarray, y_fit: np.ndarray, weights: Optional[np.ndarray] = None) -> float:
    """
    Return mean squared error (MSE) of y and y_fit, $\sum (y-y_fit)**2/N$

    Args:
        y (np.array): real data
        y_fit (np.array): estimation or fitting of data
        weights (Optional[np.array], optional): the weights of data. Defaults to None.

    Returns:
        np.float64: mean squared error (MSE)
    """

    if weights is None:
        weights = np.ones_like(y)
    return np.sum((y-y_fit)**2*weights)/y.size


def get_RMSE(y: np.ndarray, y_fit: np.ndarray, weights: Optional[np.ndarray] = None) -> float:
    """
    Return root-mean-square error (RMSE) of y and y_fit, $\sqrt{\sum (y-y_fit)**2/N}$

    Args:
        y (np.array): real data
        y_fit (np.array): estimation or fitting of data
        weights (Optional[np.array], optional): the weights of data. Defaults to None.

    Returns:
        np.float64: root-mean-square error (RMSE)
    """

    if weights is None:
        weights = np.ones_like(y)
    return np.sqrt(np.sum((y-y_fit)**2*weights)/y.size)


def get_SSR(y: np.ndarray, y_fit: np.ndarray, weights: Optional[np.ndarray] = None) -> float:
    """
    Return sum of squares of the regression (SSR) of y and y_fit, $\sum (\bar y-y_fit)**2/N$

    Args:
        y (np.array): real data
        y_fit (np.array): estimation or fitting of data
        weights (Optional[np.array], optional): the weights of data. Defaults to None.

    Returns:
        np.float64: sum of squares of the regression (SSR)
    """

    if weights is None:
        weights = np.ones_like(y)
    return np.sum((np.mean(y)-y_fit)**2*weights)


def get_SST(y: np.ndarray, weights: Optional[np.ndarray] = None) -> float:
    """
    Return total sum of square (SST) of y and y_fit, $\sum (\bar y-y)**2/N$

    Args:
        y (np.array): real data
        weights (Optional[np.array], optional): the weights of data. Defaults to None.

    Returns:
        np.float64: total sum of square (SST)
    """

    if weights is None:
        weights = np.ones_like(y)
    return np.sum((np.mean(y)-y)**2*weights)


def get_R2(y: np.ndarray, y_fit: np.ndarray, weights: Optional[np.ndarray] = None, p: int = 1,
           mode: Literal['adjust', 'original'] = 'adjust') -> float:
    """
    Return R-square, i.e. R2 or adjustR2 of y and y_fit, 1-SSE/SST=SSR/SST

    Args:
        y (np.array): real data
        y_fit (np.array): estimation or fitting of data
        weights (Optional[np.array], optional): the weights of data. Defaults to None.
        p (int, optional): the number of independent variable. Defaults to 1.
        mode (str, optional): in 'original' return R2, in 'adjust' return adjusted R2. Defaults to 'adjust'.

    Returns:
        np.float64: R2 or adjustR2
    """
    n = y.size

    if weights is None:
        weights = np.ones_like(y)

    SSE = np.sum((y-y_fit)**2*weights)
    SST = np.sum((np.mean(y)-y)**2*weights)

    assert mode in ['original', 'adjust'], 'this mode is not supported.'

    if mode in ['original']:
        return 1-SSE/SST

    return 1-SSE*(n-1)/SST/(n-p-1)

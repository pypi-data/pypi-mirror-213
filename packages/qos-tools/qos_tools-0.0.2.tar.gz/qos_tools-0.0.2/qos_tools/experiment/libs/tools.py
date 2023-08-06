# Rebuild: Liu Pei  <liupei200546@163.com>  2022/02/25

from typing import Optional

import numpy as np


def generate_spanlist_linear(center: Optional[float] = None,
                             delta: Optional[float] = None,
                             st: Optional[float] = None,
                             ed: Optional[float] = None,
                             sweep_points: int = 101,
                             **kw) -> np.ndarray:
    """
    Linear span. Two cases are allowed:
        - `center` and `delta` given, an array on (`center`-`delta`, `center`+`delta`) with sweep points equal to `sweep_points` is returned.
        - `st` for start and `ed` for end, an an array on (`st`, `ed`) with sweep points equal to `sweep_points` is returned.

    Args:
        center (Optional[float], optional): Center. Defaults to None.
        delta (Optional[float], optional): Span. Defaults to None.
        st (Optional[float], optional): Start. Defaults to None.
        ed (Optional[float], optional): End. Defaults to None.
        sweep_points (int, optional): Sweep points. Defaults to 101.

    Raises:
        ValueError: Illegal paramsters

    Returns:
        np.ndarray: 1d array of data
    """

    if center is not None and delta is not None:
        return np.linspace(center - delta, center + delta, sweep_points)
    elif st is not None and ed is not None:
        return np.linspace(st, ed, sweep_points)
    else:
        raise ValueError('The scanning interval entered is illegal')


def generate_spanlist_log(center: Optional[float] = None,
                          delta: Optional[float] = None,
                          st: Optional[float] = None,
                          ed: Optional[float] = None,
                          sweep_points: int = 101,
                          **kw) -> np.ndarray:
    """
    Log span. Three cases are allowed:
        - `center` and `delta` given, an array on (`center`-`delta`, `center`) and (`center`, `center`+`delta`) with sweep points equal to half of `sweep_points` for each is returned.
        - `st` for start and `ed` for end, an array on (`st`, `ed`) with sweep points equal to `sweep_points` is returned.
        - `st`, `ed` and `center` given, an array on (`st`, `center`) and (`center`, `ed`) with sweep points equal to half of `sweep_points` for each is returned.

    Args:
        center (Optional[float], optional): Center. Defaults to None.
        delta (Optional[float], optional): Span. Defaults to None.
        st (Optional[float], optional): Start. Defaults to None.
        ed (Optional[float], optional): End. Defaults to None.
        sweep_points (int, optional): Sweep points. Defaults to 101.

    Raises:
        ValueError: Illegal paramsters

    Returns:
        np.ndarray: 1d array of data
    """

    sweep_half = (np.logspace(0, 1, (sweep_points + 1) // 2) - 1) / 9
    if center is not None and delta is not None:
        return np.concatenate(
            (-sweep_half[::-1][:-1], sweep_half)) * delta + center
    elif st is not None and ed is not None:
        if center is None:
            center = (st + ed) / 2
            delta = (ed - st) / 2
            return np.concatenate(
                (-sweep_half[::-1][:-1], sweep_half)) * delta + center
        else:
            return np.concatenate(
                (sweep_half[::-1][:-1] * (st - center), sweep_half *
                 (ed - center))) + center
    else:
        raise ValueError('The scanning interval entered is illegal')


def generate_spanlist(mode: str = 'linear', **kw) -> np.ndarray:
    """
    Generate a span list.

    Args:
        mode (str, optional): 'linear' for linear span and 'log' for log. Defaults to 'linear'.

    Raises:
        ValueError: f'Mode {mode} is not supported.'

    Returns:
        np.ndarray: 1d array of data
    """
    if mode == 'linear':
        return generate_spanlist_linear(**kw)
    elif mode == 'log':
        return generate_spanlist_log(**kw)
    else:
        raise ValueError(f'Mode {mode} is not supported.')


def generate_log_intlist(max_int: int, sweep_points: int, min_int: float = 1) -> np.ndarray:
    """
    Generate a list of int which follows the log-uniform.

    Args:
        max_int (int): Maximum integer.
        sweep_points (int): Expected point number, but the returned on may be less than it because of unique method. 
        min_int (float, optional): Minimum integer. Defaults to 1.

    Returns:
        np.ndarray: 1d array of int
    """

    return np.unique(np.round(np.logspace(np.log10(min_int*1.0), np.log10(max_int*1.0), sweep_points))).astype(int)

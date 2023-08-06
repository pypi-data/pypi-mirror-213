# Rebuild: Liu Pei  <liupei200546@163.com>  2022/05/04

from itertools import chain
from typing import Optional, Union

import numpy as np

__all__ = [
    'RamseyLike', 'T1'
]


def RamseyLike(qubits: list[str],
               rotate: float, time_length: float, points_in_one_period: int = 10,
               name: str = 'Ramsey',
               signal: str = 'iq_avg', act_qubits: Optional[list[str]] = None, **kw) -> dict:
    """
    ['time'] SpinEcho, Ramsey, XY16, XY8, XY4, CP, CPMG and UDD circuit.

    Args:
        qubits (list[str]): the qubit name.
        rotate (float): offset of frequency.
        time_length (float): length of delay time.
        points_in_one_period (int, optional): points per period. Defaults to 10.
        signal (str, optional): signal. Defaults to 'iq_avg'.
        act_qubits (Optional[list[str]], optional): act qubits. Defaults to None.
        n(int): parameter for certain circuit via `kw`

    Returns:
        dict: config
    """

    assert name in ['SpinEcho', 'Ramsey', 'XY16', 'XY8', 'XY4',
                    'CP', 'CPMG', 'UDD', ], 'Invalid circuit type'
    kwn = {}
    if name in ['CP', 'CPMG', 'UDD']:
        kwn['n'] = kw.get('n', 1)

    act_qubits = qubits if act_qubits is None else act_qubits
    import waveforms.quantum as utils

    return {
        'init': {
            'name': name,
            'qubits': qubits,
            'signal': signal,
        },
        'sweep_setting': {
            'time': np.linspace(0, time_length, round(time_length*rotate*points_in_one_period)+1),
        },
        'sweep_addition': {
            'circuit': lambda time: [
                *chain.from_iterable(getattr(utils, name)(qubit=q,
                                     t=time, f=rotate, **kwn) for q in act_qubits),
                ('Barrier', tuple(qubits)),
                *[(('Measure', j), q) for j, q in enumerate(qubits)],
            ],
        },
    }


def T1(qubits: list[str],
       time_length: Union[float, list], mode: str = 'linear', sweep_points: int = 51,
       signal: str = 'iq_avg', act_qubits: Optional[list[str]] = None, **kw) -> dict:
    """
    [f'{q}'] T1.

    Args:
        qubits (list[str]): the qubit name.
        time_length (Union[float, list]): the delay time length, for each qubit(in the type list of float) or for all qubits(int the type float).
        sweep_points (int, optional): sweep points. Defaults to 51.
        mode (str, optional): in ['linear' (for linear time sampling), 'log' (for log time sampling)]. Defaults to 'linear'.
        signal (str, optional): signal. Defaults to 'iq_avg'.
        act_qubits (Optional[list[str]], optional): act qubits. Defaults to None.
        signal (str, optional): signal type. Defaults to 'raw'.

    Raises:
        ValueError: The time_length is illegal.
        ValueError: [description]

    Returns:
        dict: config.
    """

    act_qubits = qubits if act_qubits is None else act_qubits

    if isinstance(time_length, list) and len(time_length) != len(qubits):
        raise ValueError('The time_length is illegal')
    elif isinstance(time_length, float):
        time_length = [time_length for _ in qubits]
    else:
        raise ValueError('The time_length is illegal')

    timeList = []
    if mode in ['log']:
        for j, _ in enumerate(qubits):
            timeList.append(np.logspace(
                1e-9, np.log10(time_length), sweep_points))
    else:
        for j, _ in enumerate(qubits):
            timeList.append(np.concatenate((np.linspace(0, time_length[j]/3, sweep_points//3*2),
                            np.linspace(time_length[j]/3, time_length[j], sweep_points-sweep_points//3*2+1)[1:])))

    return {
        'init': {
            'name': 'T1',
            'qubits': qubits,
            'signal': signal,
        },
        'sweep_setting': {
            tuple(act_qubits): tuple(timeList),
        },
        'sweep_addition': {
            'circuit': lambda **kw: [
                *[(('rfUnitary', np.pi, 0), q) for q in act_qubits],
                *[(('Delay', kw[q]), q) for q in act_qubits],
                ('Barrier', tuple(qubits)),
                *[(('Measure', j), q) for j, q in enumerate(qubits)],
            ],
        },
    }

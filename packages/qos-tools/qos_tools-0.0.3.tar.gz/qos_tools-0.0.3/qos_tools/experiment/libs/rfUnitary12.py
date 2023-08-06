# Rebuild: Liu Pei  <liupei200546@163.com>  2022/05/17

from itertools import chain
from typing import Optional

import kernel
import numpy as np

from .tools import generate_spanlist


def Spectrum(qubits: list[str],
             delta: Optional[float] = None, st: Optional[float] = None, ed: Optional[float] = None, sweep_points: int = 101, mode: str = 'linear',
             signal: str = 'iq_avg', act_qubits: Optional[list[str]] = None,
             with_other_params: list[tuple] = [], **kw) -> dict:
    """
    [f'{q}'] spectrum.

    Args:
        qubits (list[str]): the qubit name.
        delta (Optional[float], optional): sweep span. Defaults to None.
        st (Optional[float], optional): sweep start. Defaults to None.
        ed (Optional[float], optional): sweep end. Defaults to None.
        sweep_points (int, optional): sweep points. Defaults to 101.
        mode (str, optional): sample mode. Defaults to 'linear'.
        act_qubits (Optional[list[str]], optional): act qubits. Defaults to None.
        signal (str, optional): signal. Defaults to 'iq_avg'.
        with_other_params (list, optional): other params. Defaults to [].
    """

    act_qubits = qubits if act_qubits is None else act_qubits
    sweep_list = generate_spanlist(
        center=0, st=st, ed=ed, delta=delta, sweep_points=sweep_points, mode=mode)

    return {
        'init': {
            'name': 'Spectrum',
            'qubits': qubits,
            'signal': signal,
        },
        'sweep_setting': {
            tuple(act_qubits): tuple([
                kernel.get(f'gate.rfUnitary12.{q}.params.frequency')+sweep_list for q in act_qubits
            ]),
        },
        'sweep_addition': {
            'circuit': lambda **kw: [
                *[(('rfUnitary', np.pi, 0), q) for q in act_qubits],
                *[(('rfUnitary12', np.pi/2, 0,
                    ('with', ('param:frequency', kw[q]), *with_other_params)), q) for q in act_qubits],
                *[(('rfUnitary', np.pi, 0), q) for q in act_qubits],
                ('Barrier', tuple(qubits)),
                *[(('Measure', j), q) for j, q in enumerate(qubits)],
            ],
        },
    }


def PowerRabi(qubits: list[str],
              scale_times: float = 4, sweep_points: int = 21,
              signal: str = 'iq_avg', act_qubits: Optional[list[str]] = None,
              with_other_params: list[tuple] = [], **kw) -> dict:
    """
    [f'{q}'] power Rabi.

    Args:
        qubits (list[str]): the qubit name.
        scale_times (float, optional): proportion of max scale in this measure to the original. Defaults to 4.
        sweep_points (int, optional): sweep points. Defaults to 21.
        signal (str, optional): signal. Defaults to 'iq_avg'.
        act_qubits (Optional[list[str]], optional): act qubits. Defaults to None.
        with_other_params (list[tuple], optional): other params. Defaults to [].
    """

    act_qubits = qubits if act_qubits is None else act_qubits

    return {
        'init': {
            'name': 'Power Rabi',
            'qubits': qubits,
            'signal': signal,
        },
        'sweep_setting': {
            tuple(act_qubits): tuple([
                np.linspace(0, min(1, scale_times*kernel.get(f'gate.rfUnitary12.{q}.params.amp')[1][-1]), sweep_points) for q in act_qubits
            ]),
        },
        'sweep_addition': {
            'circuit': lambda **kw: [
                *[(('rfUnitary', np.pi, 0), q) for q in act_qubits],
                *[(('rfUnitary12', np.pi/2, 0,
                    ('with', ('param:amp', [[0, 0.5], [0, kw[q]]]), *with_other_params)), q) for q in act_qubits],
                *[(('rfUnitary', np.pi, 0), q) for q in act_qubits],
                ('Barrier', tuple(qubits)),
                *[(('Measure', j), q) for j, q in enumerate(qubits)],
            ],
        },
    }


def PowerRabi_n(qubits: list[str],
                n: int = 1, mode: str = 'log', sweep_points: int = 21,
                signal: str = 'iq_avg', act_qubits: Optional[list[str]] = None,
                with_other_params: list[tuple] = [], **kw) -> dict:
    """
    [f'{q}'] n pulses of power Rabi.

    Args:
        qubits (list[str]): the qubit name.
        n (int, optional): numbers of pulses. Defaults to 1.
        mode (str, optional): sample mode. Defaults to 'log'.
        sweep_points (int, optional): sweep points. Defaults to 21.
        signal (str, optional): signal. Defaults to 'iq_avg'.
        act_qubits (Optional[list[str]], optional): act qubits. Defaults to None.
        with_other_params (list[tuple], optional): other params. Defaults to [].
    """

    act_qubits = qubits if act_qubits is None else act_qubits
    scale = {q: kernel.get(f'gate.rfUnitary12.{q}.params.amp')
             [-1][-1] for q in qubits}

    return {
        'init': {
            'name': 'N Power Rabi',
            'qubits': qubits,
            'signal': signal,
        },
        'sweep_setting': {
            tuple(act_qubits): tuple([
                generate_spanlist(center=scale[q], st=scale[q]*(1-1/n), ed=min(1, scale[q]*(1+1/n)), sweep_points=sweep_points, mode=mode) for q in act_qubits
            ]),
        },
        'sweep_addition': {
            'circuit': lambda n=n, **kw: [
                *[(('rfUnitary', np.pi, 0), q) for q in act_qubits],
                *[(('rfUnitary12', np.pi/2, 0, ('with',
                                            ('param:amp', [[0, 0.5], [0, kw[q]]]), *with_other_params)), q) for q in act_qubits]*n,
                *[(('rfUnitary', np.pi, 0), q) for q in act_qubits],
                ('Barrier', tuple(qubits)),
                *[(('Measure', j), q) for j, q in enumerate(qubits)],
            ],
        },
    }


def TimeRabi(qubits: list[str],
             duration_times: float = 4, sweep_points: int = 21,
             signal: str = 'iq_avg', act_qubits: Optional[list[str]] = None,
             with_other_params: list[tuple] = [], **kw) -> dict:
    """
    [f'{q}'] time Rabi.

    Args:
        qubits (list[str]): the qubit name.
        duration_times (float, optional): proportion of max duration in this measure to the original. Defaults to 4.
        sweep_points (int, optional): sweep points. Defaults to 21.
        signal (str, optional): signal. Defaults to 'iq_avg'.
        act_qubits (Optional[list[str]], optional): act qubits. Defaults to None.
        with_other_params (list[tuple], optional): other params. Defaults to [].
    """

    act_qubits = qubits if act_qubits is None else act_qubits

    return {
        'init': {
            'name': 'Time Rabi',
            'qubits': qubits,
            'signal': signal,
        },
        'sweep_setting': {
            tuple(act_qubits): tuple([
                np.linspace(0, duration_times*kernel.get(f'gate.rfUnitary12.{q}.params.duration')[1][-1], sweep_points) for q in act_qubits
            ]),
        },
        'sweep_addition': {
            'circuit': lambda **kw: [
                *[(('rfUnitary', np.pi, 0), q) for q in act_qubits],
                *[(('rfUnitary12', np.pi/2, 0,
                    ('with', ('param:duration', [[0, 0.5], [kw[q], kw[q]]]), *with_other_params)), q) for q in act_qubits],
                *[(('rfUnitary', np.pi, 0), q) for q in act_qubits],
                ('Barrier', tuple(qubits)),
                *[(('Measure', j), q) for j, q in enumerate(qubits)],
            ],
        },
    }


def XXDelta(qubits: list[str],
            n: int = 1, bound: float = 60e6, mode: str = 'linear', sweep_points: int = 21, ini_gate=('rfUnitary12', np.pi, np.pi/2),
            signal: str = 'iq_avg', act_qubits: Optional[list[str]] = None,
            with_other_params: list[tuple] = [], **kw) -> dict:
    """
    [f'{q}'] measure DRAG delta using a sequence as 'Y'-'X'-'-X'-'X'-'-X'-...-'X'-'-X'.

    Args:
        qubits (list[str]): the qubit name.
        n (int, optional): numbers of pulses 'X' and '-X'. Defaults to 1.
        bound (float, optional): delta upper bound, actually bound/n is applied. Defaults to 60e6.
        mode (str, optional): in ['linear' (for linear time sampling), 'log' (for log time sampling)]. Defaults to 'linear'.
        sweep_points (int, optional): sweep points. Defaults to 21.
        ini_gate (tuple, optional): first gate. Defaults to ('rfUnitary', np.pi, np.pi/2).
        signal (str, optional): signal. Defaults to 'iq_avg'.
        act_qubits (Optional[list[str]], optional): act qubits. Defaults to None.
        with_other_params (list[tuple], optional): other params. Defaults to [].
    """

    act_qubits = qubits if act_qubits is None else act_qubits
    sweep_list = generate_spanlist(
        center=0, delta=bound/n, sweep_points=sweep_points, mode=mode)

    return {
        'init': {
            'name': 'X-X Delta',
            'qubits': qubits,
            'signal': signal,
        },
        'sweep_setting': {
            tuple(act_qubits): tuple([
                sweep_list+kernel.get(f'gate.rfUnitary12.{q}.params.delta') for q in act_qubits
            ]),
        },
        'sweep_addition': {
            'circuit': lambda n=n, **kw: [
                *[(('rfUnitary', np.pi, 0), q) for q in act_qubits],
                *[(ini_gate, q) for q in act_qubits],
                *chain.from_iterable(zip([*[(('rfUnitary12', np.pi/2, 0,
                                              ('with', ('param:delta', kw[q]), *with_other_params)), q) for q in act_qubits]*n],
                                         [*[(('rfUnitary12', np.pi/2, np.pi,
                                              ('with', ('param:delta', kw[q]), *with_other_params)), q) for q in act_qubits]*n])),
                *[(('rfUnitary', np.pi, 0), q) for q in act_qubits],
                ('Barrier', tuple(qubits)),
                *[(('Measure', j), q) for j, q in enumerate(qubits)],
            ],
        },
    }
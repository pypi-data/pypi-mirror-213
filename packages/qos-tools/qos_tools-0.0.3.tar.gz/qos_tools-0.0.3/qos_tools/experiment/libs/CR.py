# Rebuild: Liu Pei  <liupei200546@163.com>  2022/03/18

from itertools import chain
from typing import Optional

import kernel
import numpy as np

from .tools import generate_spanlist

__all__ = [
    'ZZRamsey',
    'CR_tomo_amp1', 'CR_tomo_others', 'CR_seq', 'CR_seq_param',
]


def _ZZ_circuit(qubit: str, neighbors: list[str],
                delay: float = 50e-9, **kw) -> list:
    """
    Generate ZZ initial circuits.

    Args:
        qubit (str): qubit observed.
        neighbors (list[str]): neighbors of the qubit.
        delay (float, optional): delay time. Defaults to 50e-9.

    Returns:
        list: initial circuits.
    """
    ret = []
    for i in range(2**(len(neighbors))):
        tmp = []
        for j in range(len(neighbors)):
            if i & (2**j):
                tmp.append(('X', neighbors[j]))
            else:
                tmp.append(('I', neighbors[j]))
        tmp.extend([('Barrier', tuple([qubit, *neighbors])),
                    (('Delay', delay), qubit),
                    ('Barrier', tuple([qubit, *neighbors]))])
        ret.append(tmp)
    return ret


def ZZRamsey(qubit: str, neighbors: list[str],
             rotate: float, time_length: float, points_in_one_period: int = 10,
             signal: str = 'population', **kw) -> dict:
    """
    ['time'] ZZ using Ramsey to watch.

    Args:
        qubit (str): qubit observed.
        neighbors (list[str]): neighbors of the qubit.
        rotate (float): offset of frequency.
        time_length (float): length of delay time.
        points_in_one_period (int, optional): points per period. Defaults to 10.
        signal (str, optional): signal. Defaults to 'population'.
    """

    from waveforms.quantum import Ramsey

    return {
        'init': {
            'name': 'ZZ Ramsey',
            'qubits': [qubit, *neighbors],
            'signal': signal,
        },
        'sweep_setting': {
            'gate': _ZZ_circuit(qubit=qubit, neighbors=neighbors, **kw),
            'time': np.linspace(0, time_length, round(time_length*rotate*points_in_one_period)+1),
        },
        'sweep_addition': {
            'circuit': lambda gate, time: [
                *gate,
                *Ramsey(qubit=qubit, t=time, f=rotate),
                (('Measure', 0), qubit),
            ],
        },
    }


def _cr_readout_list(qubits: list[tuple[str]],
                     readout: str = 'target',
                     **kw) -> list[str]:

    if readout == 'both':
        readout_qubits = chain.from_iterable(qubits)
    elif readout == 'target':
        readout_qubits = [q[1] for q in qubits]
    elif readout == 'control':
        readout_qubits = [q[0] for q in qubits]
    else:
        raise ValueError('Illegal readout type in generate a cr circuit')

    return readout_qubits


def CR_tomo_amp1(qubits: list[tuple[str]],
                 st: Optional[float] = None, ed: Optional[float] = None, sweep_points: int = 13, mode: str = 'linear',
                 tomo_time_length: float = 10, tomo_time_step: float = 0.1,
                 gate1: list = ['I', 'X'], gate2: list = ['-Y/2', 'X/2', 'I'],
                 signal: str = 'population', default_type: str = 'default', **kw) -> dict:
    """
    [Feed 'duration'] H tomography for CR as amp1 changing.

    Args:
        qubits (list[tuple[str]]): qubit names.
        st (Optional[float], optional): scale start. Defaults to None.
        ed (Optional[float], optional): scale end. Defaults to None.
        sweep_points (int, optional): sweep points. Defaults to 13.
        mode (str, optional): sampling mode. Defaults to 'linear'.
        tomo_time_length (float, optional): times of duration. Defaults to 10.
        tomo_time_step (float, optional): step of duration. Defaults to 0.1.
        gate1 (list, optional): gate on control. Defaults to ['I', 'X'].
        gate2 (list, optional): gate on target. Defaults to ['-Y/2', 'X/2', 'I'].
        signal (str, optional): signal. Defaults to 'population'.
    """

    config_type = 'params' if default_type == 'default' else default_type

    amp1 = {
        q: kernel.get(f'gate.CR.{q[0]}_{q[1]}.{default_type}.amp1') for q in qubits
    }
    strength = {
        q: kernel.get(f'gate.CR.{q[0]}_{q[1]}.{default_type}.duration')*amp1[q] for q in qubits
    }
    readout_qubits = _cr_readout_list(qubits=qubits, **kw)

    return {
        'init': {
            'name': 'CR Tomo Amp1',
            'qubits': qubits,
            'signal': signal,
        },
        'setting': {
            'feed': lambda _, step, amp1=amp1, strength=strength, qubits=qubits: step.feed(
                {
                    'duration': [
                        strength[q]/amp1[q]/step.kwds['amp1_times']*step.kwds['duration_times'] for q in qubits
                    ]
                },
                store=True),
        },
        'sweep_setting': {
            'amp1_times': generate_spanlist(st=st, ed=ed, sweep_points=sweep_points, mode=mode),
            'duration_times': np.arange(tomo_time_step, tomo_time_length + tomo_time_step, tomo_time_step),
            'gate1': gate1,
            'gate2': gate2,
        },
        'sweep_addition': {
            'circuit':
            lambda amp1_times, duration_times, gate1, gate2, amp1=amp1, strength=strength, qubits=qubits: [
                *[(gate1, q[0]) for q in qubits],
                *[(('CR', ('with',
                           ('type', default_type), 
                           ('param:duration',
                            strength[q]/amp1[q]/amp1_times*duration_times),
                           ('param:amp1', amp1[q]*amp1_times))), q) for q in qubits],
                *[(gate2, q[1]) for q in qubits],
                ('Barrier', tuple(chain.from_iterable(qubits))),
                *[(('Measure', j), q) for j, q in enumerate(readout_qubits)],
            ],
        },
    }


def CR_tomo_others(qubits: list[tuple[str]], name: str,
                   st: Optional[float] = None, ed: Optional[float] = None, mode: str = 'linear', sweep_points: int = 13,
                   tomo_time_length: float = 10, tomo_time_step: float = 0.1, duration: Optional[dict] = None,
                   gate1: list = ['I', 'X'], gate2: list = ['-Y/2', 'X/2', 'I'],
                   signal: str = 'population', multi_param: list[str] = ['amp2'], **kw) -> dict:
    """
    [Feed 'duration'] H tomography for CR as amp1 changing.

    Args:
        qubits (list[tuple[str]]): qubit names.
        name (str): name of params.
        st (Optional[float], optional): scale start. Defaults to None.
        ed (Optional[float], optional): scale end. Defaults to None.
        sweep_points (int, optional): sweep points. Defaults to 13.
        mode (str, optional): sampling mode. Defaults to 'linear'.
        tomo_time_length (float, optional): times of duration. Defaults to 10.
        tomo_time_step (float, optional): step of duration. Defaults to 0.1.
        gate1 (list, optional): gate on control. Defaults to ['I', 'X'].
        gate2 (list, optional): gate on target. Defaults to ['-Y/2', 'X/2', 'I'].
        signal (str, optional): signal. Defaults to 'population'.
        multi_param (list[str], optional): params not in `multi_param` using add mode. Defaults to ['amp2'].
    """

    sweep_list = generate_spanlist(
        st=st, ed=ed, sweep_points=sweep_points, mode=mode)

    if duration is None:
        duration = {
            q: kernel.get(f'gate.CR.{q[0]}_{q[1]}.params.duration')
            for q in qubits
        }
    para_list = []
    for q in qubits:
        if name in multi_param:
            para_list.append(
                sweep_list*kernel.get(f'gate.CR.{q[0]}_{q[1]}.params.{name}'))
        else:
            para_list.append(
                sweep_list+kernel.get(f'gate.CR.{q[0]}_{q[1]}.params.{name}'))
    readout_qubits = _cr_readout_list(qubits=qubits, **kw)

    return {
        'init': {
            'name': f'CR Tomo {name}',
            'qubits': qubits,
            'signal': signal,
        },
        'setting': {
            'feed': lambda _, step, duration=duration, qubits=qubits: step.feed(
                {
                    'duration': [
                        step.kwds['duration_times'] * duration[q]
                        for q in qubits
                    ]
                },
                store=True),
        },
        'sweep_setting': {
            tuple([
                f'{q[0]}_{q[1]}' for q in qubits
            ]): tuple(para_list),
            'duration_times': np.arange(tomo_time_step, tomo_time_length + tomo_time_step, tomo_time_step),
            'gate1': gate1,
            'gate2': gate2,
        },
        'sweep_addition': {
            'circuit': lambda duration_times, gate1, gate2, duration=duration, qubits=qubits, name=name, **kw: [
                *[(gate1, q[0]) for q in qubits],
                *[(('CR', ('with',
                           ('param:duration', duration[q] * duration_times),
                           (f'param:{name}', kw[f'{q[0]}_{q[1]}']))), q) for q in qubits],
                *[(gate2, q[1]) for q in qubits],
                ('Barrier', tuple(chain.from_iterable(qubits))),
                *[(('Measure', j), q) for j, q in enumerate(readout_qubits)],
            ],
        },
    }


def _cr_seq_circuit(qubits: list[tuple[str]],
                    seq: str = 'A', readout: str = 'target',
                    n: int = 1) -> dict:
    """
    Generate CR gates. Ref arXiv: 2106.00675.

    Args:
        qubits (list[tuple[str]]): qubits name.
        seq (str, optional): sequency type. Defaults to 'A'.
        readout (str, optional): readout type. Defaults to 'target'.
        n (int, optional): repeat number. Defaults to 1.

    Raises:
        ValueError: 'Illegal sequency type in generate a cr circuit'.
    """

    readout_qubits = _cr_readout_list(qubits=qubits, readout=readout)

    ret = []
    if seq == 'A':
        ret.extend([
            *[('X/2', q[1]) for q in qubits], *[('CR', q) for q in qubits] * n
        ])
    elif seq == 'B':
        ret.extend([
            *[('X', q[0]) for q in qubits], *[('X/2', q[1]) for q in qubits],
            *[('CR', q) for q in qubits] * n
        ])
    elif seq == 'C':
        ret.extend([
            *[('X/2', q[1]) for q in qubits], *[('CR', q) for q in qubits] * n,
            *[('Y/2', q[1]) for q in qubits]
        ])
    elif seq == 'D':
        ret.extend([
            *[('X', q[0]) for q in qubits],
            *chain.from_iterable(
                zip([*[('CR', q) for q in qubits] * n],
                    [*[(('CR', ('with', 
                    ('param:global_phase', kernel.get(f'gate.CR.{q[0]}_{q[1]}.params.global_phase')+np.pi)))
                    , q) for q in qubits] * n])),
            *[('Y/2', q[1]) for q in qubits],
        ])
    elif seq == 'E':
        ret.extend([
            *[('Y/2', q[1]) for q in qubits], *[('CR', q) for q in qubits] * n
        ])
    elif seq == 'F':
        ret.extend([
            *[('X', q[0]) for q in qubits], *[('X/2', q[1]) for q in qubits],
            *chain.from_iterable(
                zip([*[('-Y', q[1]) for q in qubits] * n],
                    [*[('CR', q) for q in qubits] * n])),
            *[('-Y/2', q[1]) for q in qubits]
        ])
    elif seq == 'G':
        ret.extend([
            *[('X/2', q[0]) for q in qubits],
            *[('CR', q) for q in qubits] * n * 2,
            *[(('Rz', n * np.pi / 2), q[0]) for q in qubits], *[('X/2', q[0])
                                                                for q in qubits]
        ])
    else:
        raise ValueError('Illegal sequency type in generate a cr circuit')

    ret.extend([('Barrier', tuple(chain.from_iterable(qubits))),
                *[(('Measure', j), q) for j, q in enumerate(readout_qubits)]])

    return ret


def CR_seq(qubits: list[tuple[str]],
           seq: str = 'A', readout: Optional[str] = None,
           max_n: int = 10, step_n: float = 1,
           signal: str = 'population', **kw) -> dict:
    """
    ['n'] Repeat N in circuit.

    Args:
        qubits (list[tuple[str]]): qubits name.
        seq (str, optional): sequency type. Defaults to 'A'.
        readout (Optional[str], optional): readout type. Defaults to None.
        max_n (int, optional): maximum of n. Defaults to 10.
        step_n (float, optional): step of n. Defaults to 1.
        signal (str, optional): signal. Defaults to 'population'.
    """

    assert seq in ['A', 'B', 'C', 'D', 'E', 'F',
                   'G'], 'Illegal sequency type in generate a cr circuit'

    if readout is None:
        readout = 'control' if seq == 'G' else 'target'
    else:
        assert readout in ['both', 'target', 'control'
                           ], 'Illegal readout type in generate a cr circuit'

    return {
        'init': {
            'name': f'CR Seq {seq}',
            'qubits': qubits,
            'signal': signal,
        },
        'sweep_setting': {
            'n': np.arange(step_n, max_n + 1, step_n),
        },
        'sweep_addition': {
            'circuit':
            lambda n: _cr_seq_circuit(
                qubits=qubits, readout=readout, seq=seq, n=n),
        },
    }


def CR_seq_param(qubits: list[tuple[str]], name: str,
                 seq: str = 'A', readout: Optional[str] = 'target',
                 max_n: int = 10, step_n: float = 1,
                 center: Optional[float] = None, delta: Optional[float] = None, st: Optional[float] = None, ed: Optional[float] = None, sweep_points: int = 101, mode: str = 'linear',
                 signal: str = 'population', multi_param: list[str] = ['amp1', 'amp2'], default_type: str = 'params', **kw) -> dict:
    """

    Args:
        qubits (list[tuple[str]]): qubits name.
        name (str): params name.
        seq (str, optional): sequency type. Defaults to 'A'.
        readout (Optional[str], optional): readout type. Defaults to None.
        max_n (int, optional): maximum of n. Defaults to 10.
        step_n (float, optional): step of n. Defaults to 1.
        center (Optional[float], optional): sweep center. Defaults to None.
        delta (Optional[float], optional): sweep span. Defaults to None.
        st (Optional[float], optional): sweep start. Defaults to None.
        ed (Optional[float], optional): sweep end. Defaults to None.
        sweep_points (int, optional): sweep points. Defaults to 101.
        mode (str, optional): sweep mode. Defaults to 'linear'.
        signal (str, optional): signal. Defaults to 'population'.
        multi_param (list[str], optional): params not in `multi_param` using add mode. Defaults to ['amp2'].
    """

    assert seq in ['A', 'B', 'C', 'D', 'E', 'F',
                   'G'], 'Illegal sequency type in generate a cr circuit'

    if readout is None:
        readout = 'control' if seq == 'G' else 'target'
    else:
        assert readout in ['both', 'target', 'control'
                           ], 'Illegal readout type in generate a cr circuit'

    sweep_list = generate_spanlist(
        center=center, delta=delta, st=st, ed=ed, sweep_points=sweep_points, mode=mode)
    para_list = []
    for q in qubits:
        if name in multi_param:
            para_list.append(
                sweep_list*kernel.get(f'gate.CR.{q[0]}_{q[1]}.{default_type}.{name}'))
        else:
            para_list.append(
                sweep_list+kernel.get(f'gate.CR.{q[0]}_{q[1]}.{default_type}.{name}'))

    return {
        'init': {
            'name': f'CR Seq {seq} {name}',
            'qubits': qubits,
            'signal': signal,
        },
        'sweep_config': {
            f'{q[0]}_{q[1]}': {'addr': f'gate.CR.{q[0]}_{q[1]}.{default_type}.{name}'} for q in qubits
        },
        'sweep_setting': {
            tuple([
                f'{q[0]}_{q[1]}' for q in qubits
            ]): tuple(para_list),
            'n': np.arange(step_n, max_n + 1, step_n),
        },
        'sweep_addition': {
            'circuit': lambda n: _cr_seq_circuit(qubits=qubits, readout=readout, seq=seq, n=n),
        },
    }

# Rebuild: Liu Pei  <liupei200546@163.com>  2022/02/25

from typing import Optional, Union

import kernel
import numpy as np

from .tools import generate_spanlist

__all__ = [
    'S21_change_lo', 'S21_change_awg',
    'Readout_frequency', 'Readout_amp', 'Scatter',
]


def S21_change_lo(qubits: list[str],
                  center: Optional[Union[float, list[float]]] = None, delta: Optional[float] = None, st: Optional[float] = None, ed: Optional[float] = None, sweep_points: int = 101, mode: str = 'linear',
                  signal: str = 'iq_avg', **kw) -> dict:
    """
    [f'{q}'] Measure S21 without constraints, change local frequency.

    Args:
        qubits (list[str]): qubit names.
        center (Optional[Union[float, list[float]]], optional): sweep center. Defaults to None.
        delta (Optional[float], optional): sweep span. Defaults to None.
        st (Optional[float], optional): sweep start. Defaults to None.
        ed (Optional[float], optional): sweep end. Defaults to None.
        sweep_points (int, optional): sweep points. Defaults to 101.
        mode (str, optional): sweep mode. Defaults to 'linear'.
        signal (str, optional): signal. Defaults to 'iq_avg'.
    """

    if center is None:
        center = [kernel.get(
            f'gate.Measure.{q}.params.frequency') for q in qubits]
    elif isinstance(center, float):
        center = [center]*len(qubits)

    sweep_list = generate_spanlist(
        center=0, delta=delta, st=st, ed=ed, sweep_points=sweep_points, mode=mode)
    measures = set(kernel.get(f'{q}.probe') for q in qubits)

    return {
        'init': {
            'name': 'S21',
            'qubits': qubits,
            'signal': signal,
        },
        'setting': {
            'compile_once': True,
            'circuit': [(('Measure', j), q) for j, q in enumerate(qubits)],
        },
        'sweep_config':
        dict(
            list({
                q: {
                    'addr': f'gate.Measure.{q}.params.frequency',
                }
                for q in qubits
            }.items()) +
            list({m: {
                'addr': f'{m}.setting.LO',
            }
                for m in measures}.items())),
        'sweep_setting': {
            tuple([
                *qubits,
                *measures,
            ]): tuple([
                *[
                    sweep_list + center[j]
                    for j, _ in enumerate(qubits)
                ],
                *[
                    sweep_list + kernel.get(f'{m}.setting.LO')
                    for m in measures
                ],
            ]),
        },
    }


def S21_change_awg(qubits: list[str],
                   center: Optional[Union[float, list[float]]] = None, delta: Optional[float] = None, st: Optional[float] = None, ed: Optional[float] = None, mode: str = 'linear', sweep_points: int = 101,
                   signal: str = 'iq_avg', **kw) -> dict:
    """
    [f'Q{i}'] Measure S21 without constraints, change awg frequency.

    Args:
        qubits (list[str]): qubit names.
        center (Optional[Union[float, list[float]]], optional): sweep center. Defaults to None.
        delta (Optional[float], optional): sweep span. Defaults to None.
        st (Optional[float], optional): sweep start. Defaults to None.
        ed (Optional[float], optional): sweep end. Defaults to None.
        sweep_points (int, optional): sweep points. Defaults to 101.
        mode (str, optional): sweep mode. Defaults to 'linear'.
        signal (str, optional): signal. Defaults to 'iq_avg'.
    """

    if center is None:
        center = [kernel.get(
            f'gate.Measure.{q}.params.frequency') for q in qubits]
    elif isinstance(center, float):
        center = [center]*len(qubits)

    sweep_list = generate_spanlist(
        center=0, delta=delta, st=st, ed=ed, sweep_points=sweep_points, mode=mode)

    return {
        'init': {
            'name': 'S21',
            'qubits': qubits,
            'signal': signal,
        },
        'setting': {
            'circuit':
            [(('Measure', j), q) for j, q in enumerate(qubits)],
        },
        'sweep_config': {
            q: {
                'addr': f'gate.Measure.{q}.params.frequency',
            }
            for q in qubits
        },
        'sweep_setting': {
            tuple(qubits): tuple([
                sweep_list + center[j]
                for j, i in enumerate(qubits)
            ]),
        },
    }


def Readout_frequency_lo(qubits: list[str],
                         center: Optional[Union[float, list[float]]] = None, delta: Optional[float] = None, st: Optional[float] = None, ed: Optional[float] = None, mode: str = 'linear', sweep_points: int = 101,
                         gate: list = [['I'], [('rfUnitary', np.pi, 0)]],
                         signal: str = 'iq', **kw) -> dict:
    """
    [f'{q}'] Read frequency measurement under 0 state and 1 state.

    Args:
        qubits (list[str]): qubit names.
        center (Optional[Union[float, list[float]]], optional): sweep center. Defaults to None.
        delta (Optional[float], optional): sweep span. Defaults to None.
        st (Optional[float], optional): sweep start. Defaults to None.
        ed (Optional[float], optional): sweep end. Defaults to None.
        sweep_points (int, optional): sweep points. Defaults to 101.
        mode (str, optional): sweep mode. Defaults to 'linear'.
        gate (list): initial gate. Defaults to ['I', ('rfUnitary', np.pi, 0)].
        signal (str, optional): signal. Defaults to 'iq'.
    """

    if center is None:
        center = [kernel.get(
            f'gate.Measure.{q}.params.frequency') for q in qubits]
    elif isinstance(center, float):
        center = [center]*len(qubits)

    sweep_list = generate_spanlist(
        center=0, delta=delta, st=st, ed=ed, sweep_points=sweep_points, mode=mode)
    measures = set(kernel.get(f'{q}.probe') for q in qubits)

    return {
        'init': {
            'name': 'Readout Frequency',
            'qubits': qubits,
            'signal': signal,
        },
        'sweep_config': dict(
            list({
                q: {
                    'addr': f'gate.Measure.{q}.params.frequency',
                } for q in qubits
            }.items())+list({
                m: {
                    'addr': f'{m}.setting.LO',
                } for m in measures
            }.items())
        ),
        'sweep_setting': {
            ('gate', 'skip'): tuple([gate, list(range(1, 1+len(gate)))]),
            tuple([
                *qubits,
                *measures,
            ]): tuple([
                *[sweep_list+center[j] for j, _ in enumerate(qubits)],
                *[sweep_list+kernel.get(f'{m}.setting.LO') for m in measures],
            ]),
        },
        'sweep_addition': {
            'circuit': lambda gate: [
                *[(gat, q) for gat in gate for q in qubits],
                ('Barrier', tuple(qubits)),
                *[(('Measure', j), q) for j, q in enumerate(qubits)],
            ],
        },
    }


def Readout_frequency_awg(qubits: list[str],
                          center: Optional[Union[float, list[float]]] = None, delta: Optional[float] = None, st: Optional[float] = None, ed: Optional[float] = None, mode: str = 'linear', sweep_points: int = 101,
                          gate: list = [['I'], [('rfUnitary', np.pi, 0)]],
                          signal: str = 'iq', **kw) -> dict:
    """
    [f'{q}'] Read frequency measurement under 0 state and 1 state.

    Args:
        qubits (list[str]): qubit names.
        center (Optional[Union[float, list[float]]], optional): sweep center. Defaults to None.
        delta (Optional[float], optional): sweep span. Defaults to None.
        st (Optional[float], optional): sweep start. Defaults to None.
        ed (Optional[float], optional): sweep end. Defaults to None.
        sweep_points (int, optional): sweep points. Defaults to 101.
        mode (str, optional): sweep mode. Defaults to 'linear'.
        gate (list): initial gate. Defaults to ['I', ('rfUnitary', np.pi, 0)].
        signal (str, optional): signal. Defaults to 'iq'.
    """

    if center is None:
        center = [kernel.get(
            f'gate.Measure.{q}.params.frequency') for q in qubits]
    elif isinstance(center, float):
        center = [center]*len(qubits)

    sweep_list = generate_spanlist(
        center=0, delta=delta, st=st, ed=ed, sweep_points=sweep_points, mode=mode)

    return {
        'init': {
            'name': 'Readout Frequency',
            'qubits': qubits,
            'signal': signal,
        },
        'sweep_setting': {
            'gate': gate,
            tuple(qubits): tuple([
                *[sweep_list+center[j] for j, _ in enumerate(qubits)],
            ]),
        },
        'sweep_addition': {
            'circuit': lambda gate, **kw: [
                *[(gat, q) for gat in gate for q in qubits],
                ('Barrier', tuple(qubits)),
                *[(('Measure', j, ('with', ('param:frequency', kw[q]))), q)
                  for j, q in enumerate(qubits)],
            ],
        },
    }


def Readout_amp(qubits: list[str],
                center: Optional[float] = None, st: Optional[float] = None, ed: Optional[float] = None, mode: str = 'linear', sweep_points: int = 101,
                gate: list = [['I'], [('rfUnitary', np.pi, 0)]],
                signal: str = 'iq', **kw) -> dict:
    """
    [f'{q}'] Read amp measurement under 0 state and 1 state. 

    Args:
        qubits (list[str]): qubit names.
        center (Optional[Union[float, list[float]]], optional): sweep center. Defaults to None.
        st (Optional[float], optional): sweep start. Defaults to None.
        ed (Optional[float], optional): sweep end. Defaults to None.
        sweep_points (int, optional): sweep points. Defaults to 101.
        mode (str, optional): sweep mode. Defaults to 'linear'.
        gate (list): initial gate. Defaults to ['I', ('rfUnitary', np.pi, 0)].
        signal (str, optional): signal. Defaults to 'iq'.
    """

    span_list = generate_spanlist(
        center=center, st=st, ed=ed, mode=mode, sweep_points=sweep_points)

    return {
        'init': {
            'name': 'Readout Amp',
            'qubits': qubits,
            'signal': signal,
        },
        'sweep_setting': {
            'gate': gate,
            tuple(qubits): tuple(span_list*kernel.get(f'gate.Measure.{q}.params.amp') for q in qubits),
        },
        'sweep_addition': {
            'circuit': lambda gate, **kw: [
                *[(gat, q) for gat in gate for q in qubits],
                ('Barrier', tuple(qubits)),
                *[(('Measure', j, ('with', ('param:frequency', kw[q]))), q)
                  for j, q in enumerate(qubits)],
            ],
        },
    }


def Scatter(qubits: list[str],
            repeat: int = 1, gate: list = [['I'], [('rfUnitary', np.pi, 0)]],
            signal: str = 'iq', **kw) -> dict:
    """
    [None] 0 state and 1 state classification.

    Args:
        qubits (list[str]): qubit names.
        repeat (int, optional): repeat times. Defaults to 1.
        gate (list, optional): applied gate. Defaults to ['I', ('rfUnitary', np.pi, 0)].
        signal (str, optional): signal. Defaults to 'iq'.
    """

    return {
        'init': {
            'name': 'Scatter',
            'qubits': qubits,
            'signal': signal,
        },
        'sweep_setting': {
            'gate': gate,
            'repeat': np.arange(repeat),
        },
        'sweep_addition': {
            'circuit': lambda gate: [
                *[(gat, q) for gat in gate for q in qubits],
                ('Barrier', tuple(qubits)),
                *[(('Measure', j), q) for j, q in enumerate(qubits)],
            ],
        },
    }


def ReadoutDelay(qubits: list[str], cavity_frequencies: dict, delay_list: list[tuple], intrinsic_delay: float,
                 pulse_time: float = 100e-9, pulse_amp: float = 1,
                 signal: float = 'population', **kw) -> dict:
    """
    ['delay'] Readout time delay.

    Args:
        qubits (list[str]): qubit names.
        cavity_frequencies (dict): cavity frequencies.
        delay_list (list[tuple]): [(st, ed, steps) pair].
        intrinsic_delay (float): intrinsic delay.
        pulse_time (float, optional): pulse duration. Defaults to 100e-9.
        pulse_amp_times (float, optional): pulse amp. Defaults to 1.
        signal (float, optional): signal. Defaults to 'population'.
    """                 
    
    from waveforms.waveform import square, mixing
    
    readout_pulse = {}
    for q in qubits:
        readout_pulse[q], _ = mixing(pulse_amp*square(pulse_time)>>(pulse_time/2), freq=cavity_frequencies[q])
        
    return {
        'init': {
            'name': 'Readout Delay',
            'qubits': qubits,
            'signal': signal,
        },
        'sweep_setting': {
            'delay': np.concatenate([np.arange(st, ed, step) for st, ed, step in delay_list]),
        },
        'sweep_addition': {
            'circuit': lambda delay: [
                *[(('Pulse', 'readoutLine.RF', readout_pulse[q]), q) for q in qubits],
                *[(('Delay', delay+intrinsic_delay), q) for q in qubits],
                *[(('rfUnitary', np.pi/2, 0), q) for q in qubits],
                *[(('Measure', j), q) for j, q in enumerate(qubits)],
            ],
        },
    }

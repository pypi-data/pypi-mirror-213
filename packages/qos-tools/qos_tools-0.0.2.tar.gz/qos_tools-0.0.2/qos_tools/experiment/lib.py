# Author: Liu Pei  <liupei200546@163.com>  2021/08/14

from itertools import chain
from typing import Optional, Union

import kernel
import numpy as np

__all__ = [
    'S21_base_change_lo_with_constrains', 'S21_base_change_lo_without_constrains', 'S21_base_change_awg', 'S21_change_lo_without_constrains',
    'Spectrum_base_change_awg_without_constrains', 'Spectrum_base_change_lo_without_constrains', 'Spectrum_base_change_lo_without_mixing_wave'
    'PowerRabi_base_scaleTimes', 'PowerRabi_base_n_pulse', 'TimeRabi_base_durationTimes',
    'T1_without_constrains',
    'Ramsey_without_constrains', 'SpinEcho_without_constrains', 'CPMG_without_constrains', 'CP_without_constrains',
    'AllXY_without_constrains', 'AllXY6and16_alpha_without_constrains', 'AllXY7and8_delta_without_constrains', 'AllXY11and12_beta_without_constrains',
    'ReadoutFrequency_without_constrains', 'ReadoutAmp_without_constrains', 'Scatter2',
    'ReadoutDelay_without_constrains', 'RTO_without_constrains', 'PiErrorOscillation_without_constrain', 'DRAGCheck_without_constrain',
    'RB_single_qubit_without_constrain', 'XEB_single_qubit_without_constrain', 'nop',
    'XXDelta_without_constrain',
]


def generate_spanlist(center: Optional[float] = None, delta: Optional[float] = None, st: Optional[float] = None, ed: Optional[float] = None,
                      sweep_points: int = 101) -> np.ndarray:

    if center is not None and delta is not None:
        return np.linspace(center-delta, center+delta, sweep_points)
    elif st is not None and ed is not None:
        return np.linspace(st, ed, sweep_points)
    else:
        raise ValueError('The scanning interval entered is illegal')


def generate_spanlist_log(center: Optional[float] = None, delta: Optional[float] = None, st: Optional[float] = None, ed: Optional[float] = None,
                          sweep_points: int = 101) -> np.ndarray:
    sweep_half = (np.logspace(0, 1, (sweep_points+1)//2)-1)/9
    if center is not None and delta is not None:
        return np.concatenate((-sweep_half[::-1][:-1], sweep_half))*delta+center
    elif st is not None and ed is not None:
        if center is None:
            center = (st+ed)/2
            delta = (ed-st)/2
            return np.concatenate((-sweep_half[::-1][:-1], sweep_half))*delta+center
        else:
            return np.concatenate((sweep_half[::-1][:-1]*(st-center), sweep_half*(ed-center)))+center
    else:
        raise ValueError('The scanning interval entered is illegal')


def generate_RB_cycle(max_cycle: int, sweep_points: int, start: float = 0):

    return np.unique(np.round(np.logspace(start, np.log10(max_cycle*1.0), sweep_points))).astype(int)


def S21_base_change_lo_with_constrains(qubits: list[int], delta: Optional[float] = None, st: Optional[float] = None, ed: Optional[float] = None,
                                       sweep_points: int = 101) -> dict:
    """
    ['delta'] Measure S21 with constraints, change local frequency.

    Args:
        qubits (list[int]): the qubit id.
        delta (Optional[float], optional): span frequency, in the unit Hz. The sweep frequency is (-delta, delta) plus measure frequency read from config. Defaults to None.
        st (Optional[float], optional): span frequency start, in the unit Hz. The sweep frequency is (st, ed) plus measure frequency read from config. Defaults to None.
        ed (Optional[float], optional): span frequency end, in the unit Hz. The sweep frequency is (st, ed) plus measure frequency read from config. Defaults to None. Defaults to None.
        sweep_points (int, optional): sweep points. Defaults to 101.

    Returns:
        dict: config.
    """

    sweep_list = generate_spanlist(
        center=0, delta=delta, st=st, ed=ed, sweep_points=sweep_points)
    measures = set(kernel.get(f'Q{i}.probe')for i in qubits)

    return {
        'init': {
            'name': 'S21',
            'qubits': qubits,
            'signal': 'raw',
            'scanner_name': 'S21_base_change_lo_with_constrains',
        },
        'setting': {
            'delta': 0,
            'qubit_frequency': {f'Q{i}': kernel.get(f'gate.Measure.Q{i}.params.frequency') for i in qubits},
            'LO_frequency': {f'{m}': kernel.get(f'{m}.setting.LO') for m in measures},
            'pre_setting': {},
            'compile_once': True,
            'circuit_type': 'cmds:qlispcmd',
            'circuit': [
                (('Measure', j), f'Q{i}') for j, i in enumerate(qubits)
            ],
        },
        'constrains': [
            *[((f'setting.qubit_frequency.Q{i}', 'setting.delta'), lambda a,
               b: a+b, f'gate.Measure.Q{i}.params.frequency') for i in qubits],
            *[((f'setting.LO_frequency.{m}', 'setting.delta'),
               lambda a, b: a+b, f'{m}.setting.LO') for m in measures],
        ],
        'sweep_config': {
            'delta': {
                'addr': 'setting.delta',
            },
        },
        'sweep_setting': {
            'delta': sweep_list,
        },
        'plot_setting': [
            ['Frequency', np.asarray([sweep_list for _ in qubits]), 'Hz'],
        ],
        'plot': [
            ['Frequency', 'Hz'], ['Amplitude', 'a.u.'],
        ],
    }


def S21_base_change_lo_without_constrains(qubits: list[int], delta: Optional[float] = None, st: Optional[float] = None, ed: Optional[float] = None,
                                          sweep_points: int = 101) -> dict:
    """
    [f'Q{i}'] Measure S21 without constraints, change local frequency.

    Args:
        qubits (list[int]): the qubit id.
        delta (Optional[float], optional): span frequency, in the unit Hz. The sweep frequency is (-delta, delta) plus measure frequency read from config. Defaults to None.
        st (Optional[float], optional): span frequency start, in the unit Hz. The sweep frequency is (st, ed) plus measure frequency read from config. Defaults to None.
        ed (Optional[float], optional): span frequency end, in the unit Hz. The sweep frequency is (st, ed) plus measure frequency read from config. Defaults to None. Defaults to None.
        sweep_points (int, optional): sweep points. Defaults to 101.

    Returns:
        dict: cogfig.
    """

    sweep_list = generate_spanlist(
        center=0, delta=delta, st=st, ed=ed, sweep_points=sweep_points)
    measures = set(kernel.get(f'Q{i}.probe')for i in qubits)

    return {
        'init': {
            'name': 'S21',
            'qubits': qubits,
            'signal': 'raw',
            'scanner_name': 'S21_base_change_lo_without_constrains',
        },
        'setting': {
            'pre_setting': {},
            'compile_once': True,
            'circuit_type': 'cmds:qlispcmd',
            'circuit': [
                (('Measure', j), f'Q{i}') for j, i in enumerate(qubits)
            ],
        },
        'constrains': [],
        'sweep_config': dict(
            list({
                f'Q{i}': {
                    'addr': f'gate.Measure.Q{i}.params.frequency',
                } for i in qubits
            }.items())+list({
                m: {
                    'addr': f'{m}.setting.LO',
                } for m in measures
            }.items())
        ),
        'sweep_setting': {
            tuple([
                *[f'Q{i}' for i in qubits],
                *[m for m in measures],
            ]): tuple([
                *[sweep_list+kernel.get(f'gate.Measure.Q{i}.params.frequency') for i in qubits],
                *[sweep_list+kernel.get(f'{m}.setting.LO') for m in measures],
            ]),
            
        },
        'plot_setting': [
            ['Frequency', np.asarray(
                [sweep_list+kernel.get(f'gate.Measure.Q{i}.params.frequency') for i in qubits]), 'Hz'],
        ],
        'plot': [
            ['Frequency', 'Hz'], ['Amplitude', 'a.u.'],
        ],
    }


def S21_base_change_awg(qubits: list[int], delta: Optional[float] = None, st: Optional[float] = None, ed: Optional[float] = None,
                        sweep_points: int = 101) -> dict:
    """
    [f'Q{i}'] Measure S21 without constraints, change awg frequency.

    Args:
        qubits (list[int]): the qubit id.
        delta (Optional[float], optional): span frequency, in the unit Hz. The sweep frequency is (-delta, delta) plus measure frequency read from config. Defaults to None.
        st (Optional[float], optional): span frequency start, in the unit Hz. The sweep frequency is (st, ed) plus measure frequency read from config. Defaults to None.
        ed (Optional[float], optional): span frequency end, in the unit Hz. The sweep frequency is (st, ed) plus measure frequency read from config. Defaults to None. Defaults to None.
        sweep_points (int, optional): sweep points. Defaults to 101.

    Returns:
        dict: config.
    """

    sweep_list = generate_spanlist(
        center=0, delta=delta, st=st, ed=ed, sweep_points=sweep_points)

    return {
        'init': {
            'name': 'S21',
            'qubits': qubits,
            'signal': 'raw',
            'scanner_name': 'S21_base_change_awg',
        },
        'setting': {
            'pre_setting': {},
            'compile_once': False,
            'circuit_type': 'cmds:qlispcmd',
            'circuit': [
                (('Measure', j), f'Q{i}') for j, i in enumerate(qubits)
            ],
        },
        'constrains': [],
        'sweep_config': {
            f'Q{i}': {
                'addr': f'gate.Measure.Q{i}.params.frequency',
            } for i in qubits
        },
        'sweep_setting': {
            tuple([
                f'Q{i}' for i in qubits
            ]): tuple([
                sweep_list+kernel.get(f'gate.Measure.Q{i}.params.frequency') for i in qubits
            ]),
        },
        'plot_setting': [
            ['Frequency', np.asarray(
                [sweep_list+kernel.get(f'gate.Measure.Q{i}.params.frequency') for i in qubits]), 'Hz'],
        ],
        'plot': [
            ['Frequency', 'Hz'], ['Amplitude', 'a.u.'],
        ],
    }


def S21_change_lo_without_constrains(qubits: list[int], center: Optional[float] = None, delta: Optional[float] = None, st: Optional[float] = None,
                                     ed: Optional[float] = None, sweep_points: int = 101, sideband: Optional[float] = None) -> dict:
    """
    [f'Q{i}'] Measure S21 without constraints, change lo frequency.

    Args:
        qubits (list[int]): the qubit id.
        center (Optional[float], optional): center frequency, in the unit Hz. Defaults to None.
        delta (Optional[float], optional): span frequency, in the unit Hz. The sweep frequency is (-delta, delta) plus measure frequency read from config. Defaults to None.
        st (Optional[float], optional): span frequency start, in the unit Hz. The sweep frequency is (st, ed) plus measure frequency read from config. Defaults to None.
        ed (Optional[float], optional): span frequency end, in the unit Hz. The sweep frequency is (st, ed) plus measure frequency read from config. Defaults to None. Defaults to None.
        sweep_points (int, optional): sweep points. Defaults to 101.
        sideband (Optional[float], optional): sideband frequency. Defaults to None.

    Raises:
        ValueError: Args sideband is None here, which is illegal

    Returns:
        dict: config.
    """

    if sideband is None:
        raise ValueError('Args sideband is None here, which is illegal')
    sweep_list = generate_spanlist(
        center=center, delta=delta, st=st, ed=ed, sweep_points=sweep_points)
    measures = set(kernel.get(f'Q{i}.probe')for i in qubits)

    return {
        'init': {
            'name': 'S21',
            'qubits': qubits,
            'signal': 'raw',
            'scanner_name': 'S21_change_lo_without_constrains',
        },
        'setting': {
            'pre_setting': {},
            'compile_once': False,
            'circuit_type': 'cmds:qlispcmd',
            'circuit': [
                (('Measure', j), f'Q{i}') for j, i in enumerate(qubits)
            ],
        },
        'constrains': [],
        'sweep_config': dict(
            list({
                f'Q{i}': {
                    'addr': f'gate.Measure.Q{i}.params.frequency',
                } for i in qubits
            }.items())+list({
                m: {
                    'addr': f'{m}.setting.LO',
                } for m in measures
            }.items())
        ),
        'sweep_setting': {
            tuple([
                *[f'Q{i}' for i in qubits],
                *[m for m in measures],
            ]): [
                *[sweep_list for _ in qubits],
                *[sweep_list-sideband for _ in measures],
            ],
        },
        'plot_setting': [
            ['Frequency', np.asarray(
                [sweep_list+kernel.get(f'gate.Measure.Q{i}.params.frequency') for i in qubits]), 'Hz'],
        ],
        'plot': [
            ['Frequency', 'Hz'], ['Amplitude', 'a.u.'],
        ],
    }


def Spectrum_base_change_awg_without_constrains(qubits: list[int], delta: Optional[float] = None, st: Optional[float] = None, ed: Optional[float] = None,
                                                sweep_points: int = 101, pre_amp: Optional[float] = None, pre_duration: Optional[float] = None,
                                                pre_shape: Optional[str] = 'square', pre_alpha: Optional[float] = 1, pre_beta: Optional[float] = 0, pre_delta: Optional[float] = 0) -> dict:
    """
    [f'Q{i}'] Changing AWG waveform to measure spectrum.

    Args:
        qubits (list[int]): the qubit id.
        delta (Optional[float], optional): span frequency, in the unit Hz. The sweep frequency is (-delta, delta) plus measure frequency read from config. Defaults to None.
        st (Optional[float], optional): span frequency start, in the unit Hz. The sweep frequency is (st, ed) plus measure frequency read from config. Defaults to None.
        ed (Optional[float], optional): span frequency end, in the unit Hz. The sweep frequency is (st, ed) plus measure frequency read from config. Defaults to None. Defaults to None.
        sweep_points (int, optional): sweep points. Defaults to 101.
        pre_amp (Optional[float], optional): presetting drive amplitude, only valid in this measure. Defaults to None.
        pre_duration (Optional[float], optional): presetting drive duration, only valid in this measure. Defaults to None.
        pre_shape (Optional[str], optional): presetting drive shape, only valid in this measure. Defaults to 'square'.
        pre_alpha (Optional[float], optional): presetting drag alpha parameter, only valid in this measure. Defaults to 1.
        pre_beta (Optional[float], optional): presetting drag beta parameter, only valid in this measure. Defaults to 1.
        pre_delta (Optional[float], optional): presetting drag delta parameter, only valid in this measure. Defaults to 1.

    Returns:
        dict: config.
    """

    pre_setting_amp = {} if pre_amp is None else {
        f'gate.rfUnitary.Q{i}.params.amp': [[0, 0.5], [0, pre_amp]] for i in qubits
    }
    pre_setting_duration = {} if pre_duration is None else {
        f'gate.rfUnitary.Q{i}.params.duration': [[0, 0.5], [pre_duration, pre_duration]] for i in qubits
    }
    pre_setting_shape = {} if pre_shape is None else {
        f'gate.rfUnitary.Q{i}.params.shape': pre_shape for i in qubits
    }
    pre_setting_alpha = {} if pre_alpha is None else {
        f'gate.rfUnitary.Q{i}.params.alpha': pre_alpha for i in qubits
    }
    pre_setting_beta = {} if pre_beta is None else {
        f'gate.rfUnitary.Q{i}.params.beta': pre_beta for i in qubits
    }
    pre_setting_delta = {} if pre_delta is None else {
        f'gate.rfUnitary.Q{i}.params.delta': pre_delta for i in qubits
    }

    sweep_list = generate_spanlist(
        center=0, delta=delta, st=st, ed=ed, sweep_points=sweep_points)

    return {
        'init': {
            'name': 'Spectrum',
            'qubits': qubits,
            'signal': 'raw',
            'scanner_name': 'Spectrum_base_change_awg_without_constrains',
        },
        'setting': {
            'pre_setting': dict(
                list(pre_setting_amp.items())+list(
                    pre_setting_duration.items())+list(
                        pre_setting_shape.items())+list(pre_setting_alpha.items())+list(pre_setting_beta.items())+list(pre_setting_delta.items())),
            'compile_once': False,
            'circuit_type': 'cmds:qlispcmd',
            'circuit': [
                *[(('rfUnitary', np.pi, 0), f'Q{i}') for i in qubits],
                ('Barrier', tuple(f'Q{i}' for i in qubits)),
                *[(('Measure', j), f'Q{i}') for j, i in enumerate(qubits)],
            ],
        },
        'constrains': [],
        'sweep_config': {
            f'Q{i}': {
                'addr': f'gate.rfUnitary.Q{i}.params.frequency',
            } for i in qubits
        },
        'sweep_setting': {
            tuple([
                f'Q{i}' for i in qubits
            ]):  tuple([
                sweep_list+kernel.get(f'gate.rfUnitary.Q{i}.params.frequency') for i in qubits
            ]),
        },
        'plot_setting': [
            ['Frequency', np.asarray(
                [sweep_list+kernel.get(f'gate.rfUnitary.Q{i}.params.frequency') for i in qubits]), 'Hz'],
        ],
        'plot': [
            ['Frequency', 'Hz'], ['Amplitude', 'a.u.'],
        ],
    }


def Spectrum_base_change_lo_without_constrains(qubits: list[int], delta: Optional[float] = None, st: Optional[float] = None, ed: Optional[float] = None,
                                               sweep_points: int = 101, pre_amp: Optional[float] = None, pre_duration: Optional[float] = None,
                                               pre_shape: Optional[str] = 'square', pre_alpha: Optional[float] = 1, pre_beta: Optional[float] = 0, pre_delta: Optional[float] = 0) -> dict:
    """
    [f'Q{i}'] Changing lo frequency to measure spectrum.

    Args:
        qubits (list[int]): the qubit id.
        delta (Optional[float], optional): span frequency, in the unit Hz. The sweep frequency is (-delta, delta) plus measure frequency read from config. Defaults to None.
        st (Optional[float], optional): span frequency start, in the unit Hz. The sweep frequency is (st, ed) plus measure frequency read from config. Defaults to None.
        ed (Optional[float], optional): span frequency end, in the unit Hz. The sweep frequency is (st, ed) plus measure frequency read from config. Defaults to None. Defaults to None.
        sweep_points (int, optional): sweep points. Defaults to 101.
        pre_amp (Optional[float], optional): presetting drive amplitude, only valid in this measure. Defaults to None.
        pre_duration (Optional[float], optional): presetting drive duration, only valid in this measure. Defaults to None.
        pre_shape (Optional[str], optional): presetting drive shape, only valid in this measure. Defaults to 'square'.
        pre_alpha (Optional[float], optional): presetting drag alpha parameter, only valid in this measure. Defaults to 1.
        pre_beta (Optional[float], optional): presetting drag beta parameter, only valid in this measure. Defaults to 1.
        pre_delta (Optional[float], optional): presetting drag delta parameter, only valid in this measure. Defaults to 1.

    Returns:
        dict: config.
    """

    pre_setting_amp = {} if pre_amp is None else {
        f'gate.rfUnitary.Q{i}.params.amp': [[0, 0.5], [0, pre_amp]] for i in qubits
    }
    pre_setting_duration = {} if pre_duration is None else {
        f'gate.rfUnitary.Q{i}.params.duration': [[0, 0.5], [pre_duration, pre_duration]] for i in qubits
    }
    pre_setting_shape = {} if pre_shape is None else {
        f'gate.rfUnitary.Q{i}.params.shape': pre_shape for i in qubits
    }
    pre_setting_alpha = {} if pre_alpha is None else {
        f'gate.rfUnitary.Q{i}.params.alpha': pre_alpha for i in qubits
    }
    pre_setting_beta = {} if pre_beta is None else {
        f'gate.rfUnitary.Q{i}.params.beta': pre_beta for i in qubits
    }
    pre_setting_delta = {} if pre_delta is None else {
        f'gate.rfUnitary.Q{i}.params.delta': pre_delta for i in qubits
    }

    sweep_list = generate_spanlist(
        center=0, delta=delta, st=st, ed=ed, sweep_points=sweep_points)

    return {
        'init': {
            'name': 'Spectrum',
            'qubits': qubits,
            'signal': 'raw',
            'scanner_name': 'Spectrum_base_change_lo_without_constrains',
        },
        'setting': {
            'pre_setting': dict(
                list(pre_setting_amp.items())+list(
                    pre_setting_duration.items())+list(
                        pre_setting_shape.items())+list(pre_setting_alpha.items())+list(pre_setting_beta.items())+list(pre_setting_delta.items())),
            'compile_once': True,
            'circuit_type': 'cmds:qlispcmd',
            'circuit': [
                *[(('rfUnitary', np.pi, 0), f'Q{i}') for i in qubits],
                ('Barrier', tuple(f'Q{i}' for i in qubits)),
                *[(('Measure', j), f'Q{i}') for j, i in enumerate(qubits)],
            ],
        },
        'constrains': [],
        'sweep_config': dict(list({
            f'Q{i}': {
                'addr': f'gate.rfUnitary.Q{i}.params.frequency',
            } for i in qubits
        }.items())+list({
            f'LO{i}': {
                'addr': f'Q{i}.setting.LO',
            } for i in qubits
        }.items())),
        'sweep_setting': {
            tuple([
                *[f'Q{i}' for i in qubits],
                *[f'LO{i}' for i in qubits],
            ]): tuple([
                *[sweep_list+kernel.get(f'gate.rfUnitary.Q{i}.params.frequency') for i in qubits],
                *[sweep_list+kernel.get(f'Q{i}.setting.LO') for i in qubits],
            ]),
        },
        'plot_setting': [
            ['Frequency', np.asarray(
                [sweep_list+kernel.get(f'gate.rfUnitary.Q{i}.params.frequency') for i in qubits]), 'Hz'],
        ],
        'plot': [
            ['Frequency', 'Hz'], ['Amplitude', 'a.u.'],
        ],
    }


def Spectrum_base_change_lo_without_mixing_wave(qubits: list[int], delta: Optional[float] = None, st: Optional[float] = None, ed: Optional[float] = None,
                                                sweep_points: int = 101, pre_amp: Optional[float] = None, pre_duration: Optional[float] = None,
                                                pre_shape: Optional[str] = 'square', pre_alpha: Optional[float] = 1, pre_beta: Optional[float] = 0, pre_delta: Optional[float] = 0) -> dict:
    """
    [f'Q{i}'] Changing lo frequency to measure spectrum without any mixing frquency.

    Args:
        qubits (list[int]): the qubit id.
        delta (Optional[float], optional): span frequency, in the unit Hz. The sweep frequency is (-delta, delta) plus measure frequency read from config. Defaults to None.
        st (Optional[float], optional): span frequency start, in the unit Hz. The sweep frequency is (st, ed) plus measure frequency read from config. Defaults to None.
        ed (Optional[float], optional): span frequency end, in the unit Hz. The sweep frequency is (st, ed) plus measure frequency read from config. Defaults to None. Defaults to None.
        sweep_points (int, optional): sweep points. Defaults to 101.
        pre_amp (Optional[float], optional): presetting drive amplitude, only valid in this measure. Defaults to None.
        pre_duration (Optional[float], optional): presetting drive duration, only valid in this measure. Defaults to None.
        pre_shape (Optional[str], optional): presetting drive shape, only valid in this measure. Defaults to 'square'.
        pre_alpha (Optional[float], optional): presetting drag alpha parameter, only valid in this measure. Defaults to 1.
        pre_beta (Optional[float], optional): presetting drag beta parameter, only valid in this measure. Defaults to 1.
        pre_delta (Optional[float], optional): presetting drag delta parameter, only valid in this measure. Defaults to 1.

    Returns:
        dict: config.
    """

    pre_setting_amp = {} if pre_amp is None else {
        f'gate.rfUnitary.Q{i}.params.amp': [[0, 0.5], [0, pre_amp]] for i in qubits
    }
    pre_setting_duration = {} if pre_duration is None else {
        f'gate.rfUnitary.Q{i}.params.duration': [[0, 0.5], [pre_duration, pre_duration]] for i in qubits
    }
    pre_setting_shape = {} if pre_shape is None else {
        f'gate.rfUnitary.Q{i}.params.shape': pre_shape for i in qubits
    }
    pre_setting_alpha = {} if pre_alpha is None else {
        f'gate.rfUnitary.Q{i}.params.alpha': pre_alpha for i in qubits
    }
    pre_setting_beta = {} if pre_beta is None else {
        f'gate.rfUnitary.Q{i}.params.beta': pre_beta for i in qubits
    }
    pre_setting_delta = {} if pre_delta is None else {
        f'gate.rfUnitary.Q{i}.params.delta': pre_delta for i in qubits
    }

    sweep_list = generate_spanlist(
        center=0, delta=delta, st=st, ed=ed, sweep_points=sweep_points)

    lo_set = set()
    for i in qubits:
        lo = kernel.get(f'Q{i}.setting.LO')
        assert lo not in lo_set, 'Different qubits have the same local, which is not allowed.'
        lo_set.add(lo)

    return {
        'init': {
            'name': 'Spectrum',
            'qubits': qubits,
            'signal': 'raw',
            'scanner_name': 'Spectrum_base_change_lo_without_mixing_wave',
        },
        'setting': {
            'pre_setting': dict(
                list(pre_setting_amp.items())+list(
                    pre_setting_duration.items())+list(
                        pre_setting_shape.items())+list(pre_setting_alpha.items())+list(pre_setting_beta.items())+list(pre_setting_delta.items())),
            'compile_once': True,
            'circuit_type': 'cmds:qlispcmd',
            'circuit': [
                *[(('rfUnitary', np.pi, 0), f'Q{i}') for i in qubits],
                ('Barrier', tuple(f'Q{i}' for i in qubits)),
                *[(('Measure', j), f'Q{i}') for j, i in enumerate(qubits)],
            ],
        },
        'constrains': [],
        'sweep_config': dict(list({
            f'Q{i}': {
                'addr': f'gate.rfUnitary.Q{i}.params.frequency',
            } for i in qubits
        }.items())+list({
            f'LO{i}': {
                'addr': f'Q{i}.setting.LO',
            } for i in qubits
        }.items())),
        'sweep_setting': {
            tuple([
                *[f'Q{i}' for i in qubits],
                *[f'LO{i}' for i in qubits],
            ]): [
                *[sweep_list+kernel.get(f'gate.rfUnitary.Q{i}.params.frequency') for i in qubits],
                *[sweep_list+kernel.get(f'gate.rfUnitary.Q{i}.params.frequency') for i in qubits],
            ],
        },
        'plot_setting': [
            ['Frequency', np.asarray(
                [sweep_list+kernel.get(f'gate.rfUnitary.Q{i}.params.frequency') for i in qubits]), 'Hz'],
        ],
        'plot': [
            ['Frequency', 'Hz'], ['Amplitude', 'a.u.'],
        ],
    }


def PowerRabi_base_scaleTimes(qubits: list[int], sweep_points: int = 21, scale_times: float = 4, pre_duration: Optional[float] = None,
                              signal: str = 'raw') -> dict:
    """
    [f'Q{i}'] power Rabi.

    Args:
        qubits (list[int]): the qubit id.
        sweep_points (int, optional): sweep points. Defaults to 21.
        scale_times (float, optional): raion of max scale in this measure to the original. Defaults to 4.
        pre_duration (Optional[float], optional): presetting drive duration. Defaults to None.
        signal (str, optional): signal type. Defaults to 'raw'.

    Returns:
        dict: config.
    """

    pre_setting_duration = {} if pre_duration is None else {
        f'gate.rfUnitary.Q{i}.params.duration': [[0, 1], [pre_duration, pre_duration]] for i in qubits
    }

    return {
        'init': {
            'name': 'PowerRabi',
            'qubits': qubits,
            'signal': signal,
            'scanner_name': 'PowerRabi_base_scaleTimes',
        },
        'setting': {
            'pre_setting': pre_setting_duration,
            'compile_once': False,
            'circuit_type': 'cmds:qlispcmd',
            'circuit': [
                *[(('rfUnitary', np.pi, 0), f'Q{i}') for i in qubits],
                ('Barrier', tuple(f'Q{i}' for i in qubits)),
                *[(('Measure', j), f'Q{i}') for j, i in enumerate(qubits)],
            ],
        },
        'constrains': [],
        'sweep_config': dict(list({
            f'Q{i}_amp': {
                'addr': f'gate.rfUnitary.Q{i}.params.amp',
            } for i in qubits
        }.items())+list({
            f'Q{i}': {
                'addr': None,
            } for i in qubits
        }.items())),
        'sweep_setting': {
            tuple([
                f'Q{i}' for i in qubits
            ]): tuple([
                np.linspace(0, min(1, scale_times*kernel.get(f'gate.rfUnitary.Q{i}.params.amp')[1][-1]), sweep_points) for i in qubits
            ]),
        },
        'sweep_addition': {
            f'Q{i}_amp': lambda i=i, **kw: [[0, 0.5], [0, kw[f'Q{i}']]] for i in qubits
        },
        'plot_setting': [
            ['Scale', np.asarray([np.linspace(0, min(1, scale_times*kernel.get(f'gate.rfUnitary.Q{i}.params.amp')[1][-1]), sweep_points) for i in qubits]),
             'a.u.'],
        ],
        'plot': [
            ['Scale', 'a.u.'], ['Probability' if signal ==
                                'state' else 'Amplitude', 'a.u.'],
        ],
    }


def PowerRabi_base_n_pulse(qubits: list[int], sweep_points: int = 21, n: int = 1, signal: str = 'raw', mode: str = 'log') -> dict:
    """
    [f'Q{i}'] n pulses of power Rabi.

    Args:
        qubits (list[int]): the qubit id.
        sweep_points (int, optional): sweep points. Defaults to 21.
        n (int, optional): numbers of pulses. Defaults to 1.
        mode (str, optional): in ['linear' (for linear time sampling), 'log' (for log time sampling)]. Defaults to 'linear'.

    Returns:
        dict: config.
    """

    sweep_list = []
    if mode=='linear':
        for i in qubits:
            scale = kernel.get(f'gate.rfUnitary.Q{i}.params.amp')[-1][-1]
            sweep_list.append(np.linspace((1-1/n)*scale, min(1, (1+1/n)*scale), sweep_points))
    elif mode=='log':
        for i in qubits:
            scale = kernel.get(f'gate.rfUnitary.Q{i}.params.amp')[-1][-1]
            sweep_list.append(generate_spanlist_log(center=scale, st=scale*(1-1/n), ed=min(1, scale*(1+1/n)), sweep_points=sweep_points))
    else:
        raise ValueError(f'Mode {mode} is not supported.')

    return {
        'init': {
            'name': 'PowerRabi',
            'qubits': qubits,
            'signal': signal,
            'scanner_name': 'PowerRabi_base_n_pulse'
        },
        'setting': {
            'pre_setting': {},
            'compile_once': False,
            'circuit_type': 'cmds:qlispcmd',
            'circuit': [
                *[(('rfUnitary', np.pi, 0), f'Q{i}') for i in qubits]*n,
                ('Barrier', tuple(f'Q{i}' for i in qubits)),
                *[(('Measure', j), f'Q{i}') for j, i in enumerate(qubits)],
            ],
        },
        'constrains': [],
        'sweep_config': dict(list({
            f'Q{i}_amp': {
                'addr': f'gate.rfUnitary.Q{i}.params.amp',
            } for i in qubits
        }.items())+list({
            f'Q{i}': {
                'addr': None,
            } for i in qubits
        }.items())),
        'sweep_setting': {
            tuple([
                f'Q{i}' for i in qubits
            ]): tuple([
                sweep_list[j] for j, i in enumerate(qubits)
            ]),
        },
        'sweep_addition': {
            f'Q{i}_amp': lambda i=i, **kw: [[0, 0.5], [0.00001, kw[f'Q{i}']]] for i in qubits
        },
        'plot_setting': [
            ['Scale', np.asarray(sweep_list), 'a.u.'],
        ],
        'plot': [
            ['Scale', 'a.u.'], ['Probability' if signal ==
                                'state' else 'Amplitude', 'a.u.'],
        ],
    }


def TimeRabi_base_durationTimes(qubits: list[int], sweep_points: int = 51, duration_times: float = 4, pre_amp: Optional[float] = None,
                                signal: str = 'raw') -> dict:
    """
    [f'Q{i}'] time Rabi.

    Args:
        qubits (list[int]): the qubit id.
        sweep_points (int, optional): sweep points. Defaults to 51.
        scale_times (float, optional): raion of max scale in this measure to the original. Defaults to 4.
        pre_duration (Optional[float], optional): presetting drive duration. Defaults to None.
        signal (str, optional): signal type. Defaults to 'raw'.

    Returns:
        dict: config.
    """

    pre_setting_amp = {} if pre_amp is None else {
        f'gate.rfUnitary.Q{i}.params.amp': [[0, 1], [0, pre_amp]] for i in qubits
    }

    return {
        'init': {
            'name': 'TimeRabi',
            'qubits': qubits,
            'signal': signal,
            'scanner_name': 'TimeRabi_base_durationTimes',
        },
        'setting': {
            'pre_setting': pre_setting_amp,
            'compile_once': False,
            'circuit_type': 'cmds:qlispcmd',
            'circuit': [
                *[(('Delay', 20e-6), f'Q{i}') for i in qubits],
                *[(('rfUnitary', np.pi, 0), f'Q{i}') for i in qubits],
                ('Barrier', tuple(f'Q{i}' for i in qubits)),
                *[(('Measure', j), f'Q{i}') for j, i in enumerate(qubits)],
            ],
        },
        'constrains': [],
        'sweep_config': dict(list({
            f'Q{i}_duration': {
                'addr': f'gate.rfUnitary.Q{i}.params.duration',
            } for i in qubits
        }.items())+list({
            f'Q{i}': {
                'addr': None,
            } for i in qubits
        }.items())),
        'sweep_setting': {
            tuple([
                f'Q{i}' for i in qubits
            ]): tuple([
                np.linspace(2e-9, 2e-9+duration_times*kernel.get(f'gate.rfUnitary.Q{i}.params.duration')[1][-1], sweep_points) for i in qubits
            ]),
        },
        'sweep_addition': {
            f'Q{i}_duration': lambda i=i, **kw: [[0, 1], [kw[f'Q{i}'], kw[f'Q{i}']]] for i in qubits
        },
        'plot_setting': [
            ['Time', np.asarray([np.linspace(0,
                                             duration_times*kernel.get(f'gate.rfUnitary.Q{i}.params.duration')[1][-1], sweep_points) for i in qubits]), 's'],
        ],
        'plot': [
            ['Time', 's'], ['Probability' if signal ==
                            'state' else 'Amplitude', 'a.u.'],
        ],
    }


def Ramsey_without_constrains(qubits: list[int], rotate: float, time_length: float, points_in_one_period: int = 10, signal: str = 'raw') -> dict:
    """
    ['time'] Ramsey.

    Args:
        qubits (list[int]): the qubit id.
        rotate (float): offset of frequency.
        time_length (float): length of delay time.
        points_in_one_period (int, optional): points per period. Defaults to 10.
        signal (str, optional): signal type. Defaults to 'raw'.

    Returns:
        dict: config.
    """

    from waveforms.quantum import Ramsey

    return {
        'init': {
            'name': 'Ramsey',
            'qubits': qubits,
            'signal': signal,
            'scanner_name': 'Ramsey_without_constrains',
        },
        'setting': {
            'pre_setting': {},
            'compile_once': False,
            'circuit_type': 'cmds:qlispcmd',
            'circuit': [],
        },
        'constrains': [],
        'sweep_config': {
            'time': {
                'addr': None,
            },
            'circuit': {
                'addr': 'setting.circuit',
            },
        },
        'sweep_setting': {
            'time': np.linspace(0, time_length, round(time_length*rotate*points_in_one_period)+1),
        },
        'sweep_addition': {
            'circuit': lambda time: [
                *[(('Delay', 20e-6), f'Q{i}') for i in qubits],
                *chain.from_iterable(Ramsey(qubit=f'Q{i}', t=time, f=rotate) for i in qubits),
                ('Barrier', tuple(f'Q{i}' for i in qubits)),
                *[(('Measure', j), f'Q{i}') for j, i in enumerate(qubits)],
            ],
        },
        'plot_setting': [
            ['Time', np.asarray([np.linspace(0, time_length, round(
                time_length*rotate*points_in_one_period)+1) for _ in qubits]), 's'],
        ],
        'plot': [
            ['Delay', 's'], ['Probability' if signal ==
                             'state' else 'Amplitude', 'a.u.'],
        ],
    }


def T1_without_constrains(qubits: list[int], time_length: Union[float, list], sweep_points: int = 51, mode: str = 'linear', signal: str = 'raw') -> dict:
    """
    ['f'Q{i}'] T1 Measure.

    Args:
        qubits (list[int]): the qubit id.
        time_length (Union[float, list]): the delay time length, for each qubit(in the type list of float) or for all qubits(int the type float).
        sweep_points (int, optional): sweep points. Defaults to 51.
        mode (str, optional): in ['linear' (for linear time sampling), 'log' (for log time sampling)]. Defaults to 'linear'.
        step (float, optional): the minimum step size in log time sampling. Defaults to 16e-9.
        signal (str, optional): signal type. Defaults to 'raw'.

    Raises:
        ValueError: The time_length is illegal.
        ValueError: [description]

    Returns:
        dict: config.
    """

    if isinstance(time_length, list) and len(time_length) != len(qubits):
        raise ValueError('The time_length is illegal')
    elif isinstance(time_length, float):
        time_length = [time_length for _ in qubits]
    else:
        raise ValueError('The time_length is illegal')

    timeList = []
    if mode in ['log']:
        for j, i in enumerate(qubits):
            sr = kernel.get(f'Q{i}.waveform.SR')
            timeList.append(np.logspace(
                0, np.log10(time_length*sr), sweep_points)/sr)
    else:
        for j, i in enumerate(qubits):
            timeList.append(np.concatenate((np.linspace(0, time_length[j]/3, sweep_points//3*2),
                            np.linspace(time_length[j]/3, time_length[j], sweep_points-sweep_points//3*2+1)[1:])))

    return {
        'init': {
            'name': 'T1',
            'qubits': qubits,
            'signal': signal,
            'scanner_name': 'T1_without_constrains',
        },
        'setting': {
            'pre_setting': {},
            'compile_once': False,
            'circuit_type': 'cmds:qlispcmd',
            'circuit': [],
        },
        'constrains': [],
        'sweep_config': dict(list({
            f'Q{i}': {
                'addr': None,
            } for i in qubits
        }.items())+list({
            'circuit': {
                'addr': f'setting.circuit',
            },
        }.items())),
        'sweep_setting': {
            tuple([
                f'Q{i}' for i in qubits
            ]): tuple([
                timeList[j] for j, i in enumerate(qubits)
            ]),
        },
        'sweep_addition': {
            'circuit': lambda **kw: [
                *[(('rfUnitary', np.pi, 0), f'Q{i}') for i in qubits],
                *[(('Delay', kw[f'Q{i}']), f'Q{i}')
                  for j, i in enumerate(qubits)],
                ('Barrier', tuple(f'Q{i}' for i in qubits)),
                *[(('Measure', j), f'Q{i}') for j, i in enumerate(qubits)],
            ],
        },
        'plot_setting': [
            ['Time', np.asarray(timeList), 's'],
        ],
        'plot': [
            ['Delay', 's'], ['Probability' if signal ==
                             'state' else 'Amplitude', 'a.u.'],
        ],
    }


def SpinEcho_without_constrains(qubits: list[int], rotate: float, time_length: float, points_in_one_period: int = 10, signal: str = 'raw') -> dict:
    """
    ['time'] Spin echo.

    Args:
        qubits (list[int]): the qubit id.
        rotate (float): offset of frequency.
        time_length (float): length of delay time.
        points_in_one_period (int, optional): points per period. Defaults to 10.
        signal (str, optional): signal type. Defaults to 'raw'.

    Returns:
        dict: config.
    """

    from waveforms.quantum import SpinEcho

    return {
        'init': {
            'name': 'SpinEcho',
            'qubits': qubits,
            'signal': signal,
            'scanner_name': 'SpinEcho_without_constrains',
        },
        'setting': {
            'pre_setting': {},
            'compile_once': False,
            'circuit_type': 'cmds:qlispcmd',
            'circuit': [],
        },
        'constrains': [],
        'sweep_config': {
            'time': {
                'addr': None,
            },
            'circuit': {
                'addr': 'setting.circuit',
            },
        },
        'sweep_setting': {
            'time': np.linspace(0, time_length, round(time_length*rotate*points_in_one_period)+1),
        },
        'sweep_addition': {
            'circuit': lambda time: [
                *chain.from_iterable(SpinEcho(qubit=f'Q{i}', t=time, f=rotate) for i in qubits),
                ('Barrier', tuple(f'Q{i}' for i in qubits)),
                *[(('Measure', j), f'Q{i}') for j, i in enumerate(qubits)],
            ],
        },
        'plot_setting': [
            ['Time', np.asarray([np.linspace(0, time_length, round(
                time_length*rotate*points_in_one_period)+1) for _ in qubits]), 's'],
        ],
        'plot': [
            ['Delay', 's'], ['Probability' if signal ==
                             'state' else 'Amplitude', 'a.u.'],
        ],
    }


def CPMG_without_constrains(qubits: list[int], rotate: float, time_length: float, n: int, points_in_one_period: int = 10, signal: str = 'raw') -> dict:
    """
    ['time'] CPMG.

    Args:
        qubits (list[int]): the qubit id.
        rotate (float): offset of frequency.
        time_length (float): length of delay time.
        points_in_one_period (int, optional): points per period. Defaults to 10.
        signal (str, optional): signal type. Defaults to 'raw'.

    Returns:
        dict: config.
    """

    from waveforms.quantum import CPMG

    return {
        'init': {
            'name': 'CPMG',
            'qubits': qubits,
            'signal': signal,
            'scanner_name': 'CPMG_without_constrains',
        },
        'setting': {
            'pre_setting': {},
            'compile_once': False,
            'circuit_type': 'cmds:qlispcmd',
            'circuit': [],
        },
        'constrains': [],
        'sweep_config': {
            'time': {
                'addr': None,
            },
            'circuit': {
                'addr': 'setting.circuit',
            },
        },
        'sweep_setting': {
            'time': np.linspace(0, time_length, round(time_length*rotate*points_in_one_period)+1),
        },
        'sweep_addition': {
            'circuit': lambda time: [
                *chain.from_iterable(CPMG(qubit=f'Q{i}', t=time, f=rotate, n=n) for i in qubits),
                ('Barrier', tuple(f'Q{i}' for i in qubits)),
                *[(('Measure', j), f'Q{i}') for j, i in enumerate(qubits)],
            ],
        },
        'plot_setting': [
            ['Time', np.asarray([np.linspace(0, time_length, round(
                time_length*rotate*points_in_one_period)+1) for _ in qubits]), 's'],
        ],
        'plot': [
            ['Delay', 's'], ['Probability' if signal ==
                             'state' else 'Amplitude', 'a.u.'],
        ],
    }


def CP_without_constrains(qubits: list[int], rotate: float, time_length: float, n: int, points_in_one_period: int = 10, signal: str = 'raw') -> dict:
    """
    ['time'] CP.

    Args:
        qubits (list[int]): the qubit id.
        rotate (float): offset of frequency.
        time_length (float): length of delay time.
        points_in_one_period (int, optional): points per period. Defaults to 10.
        signal (str, optional): signal type. Defaults to 'raw'.

    Returns:
        dict: config.
    """

    from waveforms.quantum import CP

    return {
        'init': {
            'name': 'CP',
            'qubits': qubits,
            'signal': signal,
            'scanner_name': 'CP_without_constrains',
        },
        'setting': {
            'pre_setting': {},
            'compile_once': False,
            'circuit_type': 'cmds:qlispcmd',
            'circuit': [],
        },
        'constrains': [],
        'sweep_config': {
            'time': {
                'addr': None,
            },
            'circuit': {
                'addr': 'setting.circuit',
            },
        },
        'sweep_setting': {
            'time': np.linspace(0, time_length, round(time_length*rotate*points_in_one_period)+1),
        },
        'sweep_addition': {
            'circuit': lambda time: [
                *chain.from_iterable(CP(qubit=f'Q{i}', t=time, f=rotate, n=n) for i in qubits),
                ('Barrier', tuple(f'Q{i}' for i in qubits)),
                *[(('Measure', j), f'Q{i}') for j, i in enumerate(qubits)],
            ],
        },
        'plot_setting': [
            ['Time', np.asarray([np.linspace(0, time_length, round(
                time_length*rotate*points_in_one_period)+1) for _ in qubits]), 's'],
        ],
        'plot': [
            ['Delay', 's'], ['Probability' if signal ==
                             'state' else 'Amplitude', 'a.u.'],
        ],
    }


def AllXY_without_constrains(qubits: list[int], signal: str = 'raw', repeat: int = 1, n: int = 0) -> dict:
    """
    [21] AllXY 21 circuit

    Args:
        qubits (list[int]): the qubit id.
        signal (str, optional): signal type. Defaults to 'raw'.
        repeat (int, optional): repeat times. Defaults to 1.

    Returns:
        dict: config.
    """

    from waveforms.quantum import ALLXY

    def span_n(x, n, changeI: float = None):
        ret = []
        for item in x:
            n_pre = 4*n+1
            if item[0] == 'I' and changeI is not None:
                item = list(item)
                item[0] = ('Delay', changeI)
                item = tuple(item)
            if item[0] in ['X']:
                item = list(item)
                item[0] = ('rfUnitary', np.pi, 0)
                item = tuple(item)
                n_pre = 2*n+1
            if item[0] in ['Y']:
                item = list(item)
                item[0] = ('rfUnitary', np.pi, np.pi/2)
                item = tuple(item)
                n_pre = 2*n+1
            if item[0] in ['X/2']:
                item = list(item)
                item[0] = ('rfUnitary', np.pi/2, 0)
                item = tuple(item)
            if item[0] in ['Y/2']:
                item = list(item)
                item[0] = ('rfUnitary', np.pi/2, np.pi/2)
                item = tuple(item)
            ret.extend([item]*n_pre)
        return ret

    return {
        'init': {
            'name': 'AllXY',
            'qubits': qubits,
            'signal': signal,
            'scanner_name': 'AllXY_without_constrains',
            'shots': round(repeat)*1024,
        },
        'setting': {
            'pre_setting': {},
            'compile_once': False,
            'circuit_type': 'cmds:qlispcmd',
            'circuit': [],
        },
        'constrains': [],
        'sweep_config': {
            'circuit': {
                'addr': 'setting.circuit',
            },
            'number': {
                'addr': None,
            }
        },
        'sweep_setting': {
            'number': list(range(21)),
        },
        'sweep_addition': {
            'circuit': lambda number: [
                *chain.from_iterable(span_n(ALLXY(qubit=f'Q{i}', i=number), n,
                                            kernel.get(f'gate.rfUnitary.Q{i}.params.duration')[-1][-1]+kernel.get(f'gate.rfUnitary.Q{i}.params.buffer')) for i in qubits),
                ('Barrier', tuple(f'Q{i}' for i in qubits)),
                *[(('Measure', j), f'Q{i}') for j, i in enumerate(qubits)],
            ],
        },
        'plot': [
            ['Item', 'a.u.'], ['Probability' if signal ==
                               'state' else 'Amplitude', 'a.u.'],
        ],
    }


def ReadoutFrequency_without_constrains(qubits: list[int], delta: Optional[float] = None, st: Optional[float] = None, ed: Optional[float] = None,
                                        sweep_points: int = 101) -> dict:
    """
    [f'Q{i}] Read frequency measurement under 0 state and 1 state.

    Args:
        qubits (list[int]): the qubit id.
        delta (Optional[float], optional): span frequency, in the unit Hz. The sweep frequency is (-delta, delta) plus measure frequency read from config. Defaults to None.
        st (Optional[float], optional): span frequency start, in the unit Hz. The sweep frequency is (st, ed) plus measure frequency read from config. Defaults to None.
        ed (Optional[float], optional): span frequency end, in the unit Hz. The sweep frequency is (st, ed) plus measure frequency read from config. Defaults to None. Defaults to None.
        sweep_points (int, optional): sweep points. Defaults to 101.

    Returns:
        dict: config.
    """

    sweep_list = generate_spanlist(
        center=0, delta=delta, st=st, ed=ed, sweep_points=sweep_points)
    measures = set(kernel.get(f'Q{i}.probe')for i in qubits)

    return {
        'init': {
            'name': 'ReadoutFrequency',
            'qubits': qubits,
            'signal': 'raw',
            'scanner_name': 'ReadoutFrequency_without_constrains',
        },
        'setting': {
            'pre_setting': {},
            'compile_once': False,
            'circuit_type': 'cmds:qlispcmd',
            'circuit': [],
        },
        'constrains': [],
        'sweep_config': dict(
            list({
                f'Q{i}': {
                    'addr': f'gate.Measure.Q{i}.params.frequency',
                } for i in qubits
            }.items())+list({
                m: {
                    'addr': f'{m}.setting.LO',
                } for m in measures
            }.items())+list({
                'skip': {
                    'addr': f'setting.skip'
                },
                'circuit': {
                    'addr': f'setting.circuit'
                }
            }.items())
        ),
        'sweep_setting': {
            ('circuit', 'skip'): [[[
                (('Measure', j), f'Q{i}') for j, i in enumerate(qubits)
            ], [
                *[(('rfUnitary', np.pi, 0), f'Q{i}') for i in qubits],
                ('Barrier', tuple(f'Q{i}' for i in qubits)),
                *[(('Measure', j), f'Q{i}') for j, i in enumerate(qubits)]
            ], ], [1, 2]],
            tuple([
                *[f'Q{i}' for i in qubits],
                *[m for m in measures],
            ]): [
                *[sweep_list+kernel.get(f'gate.Measure.Q{i}.params.frequency') for i in qubits],
                *[sweep_list+kernel.get(f'{m}.setting.LO') for m in measures],
            ],
        },
        'plot_setting': [
            ['State', np.array([[0, 1] for _ in qubits]), 's'],
            ['Frequency', np.array(
                [sweep_list+kernel.get(f'gate.Measure.Q{i}.params.frequency') for i in qubits]), 'Hz'],
        ],
        'plot': [
            ['Frequency', 'Hz'], ['Amplitude', 'a.u.'],
        ],
    }


def ReadoutAmp_without_constrains(qubits: list[int], st: float, ed: float, sweep_points: int = 101) -> dict:
    """
    [f'Q{i}] Read amp measurement under 0 state and 1 state. 

    Args:
        qubits (list[int]): the qubit id.
        st (float, optional): span lower times bound. The sweep amp is (st, ed)*amp plus measure amp read from config.
        ed (float, optional): span upper times bound. The sweep amp is (st, ed)*amp plus measure amp read from config.
        sweep_points (int, optional): sweep points. Defaults to 101.

    Returns:
        dict: config.
    """

    return {
        'init': {
            'name': 'ReadoutAmp',
            'qubits': qubits,
            'signal': 'raw',
            'scanner_name': 'ReadoutAmp_without_constrains',
        },
        'setting': {
            'pre_setting': {},
            'compile_once': False,
            'circuit_type': 'cmds:qlispcmd',
            'circuit': [],
        },
        'constrains': [],
        'sweep_config': dict(
            list({
                f'Q{i}': {
                    'addr': f'gate.Measure.Q{i}.params.amp',
                } for i in qubits
            }.items())+list({
                'circuit': {
                    'addr': f'setting.circuit'
                }
            }.items())
        ),
        'sweep_setting': {
            'circuit': [[
                (('Measure', j), f'Q{i}') for j, i in enumerate(qubits)
            ], [
                *[(('rfUnitary', np.pi, 0), f'Q{i}') for i in qubits],
                ('Barrier', tuple(f'Q{i}' for i in qubits)),
                *[(('Measure', j), f'Q{i}') for j, i in enumerate(qubits)]
            ], ],
            tuple([
                f'Q{i}' for i in qubits
            ]): [
                np.linspace(st, ed, sweep_points)*kernel.get(f'gate.Measure.Q{i}.params.amp') for i in qubits
            ],
        },
        'plot': [
            ['Scale', 'a.u.'], ['Amplitude', 'a.u.'],
        ],
    }


def Scatter2(qubits: list[int], repeat: int = 1) -> dict:
    """
    [2] 0 state and 1 state classification.

    Args:
        qubits (list[int]): the qubit id.
        repeat (int, optional): repeat times. Defaults to 1.

    Returns:
        dict: config.
    """

    return {
        'init': {
            'name': 'Scatter2',
            'qubits': qubits,
            'signal': 'raw',
            'scanner_name': 'Scatter2',
            'shots': round(repeat)*1024
        },
        'setting': {
            'pre_setting': {},
            'compile_once': False,
            'circuit_type': 'cmds:qlispcmd',
            'circuit': [],
        },
        'constrains': [],
        'sweep_config': {
            'circuit': {
                'addr': f'setting.circuit',
            },
        },
        'sweep_setting': {
            'circuit': [[
                *[(('Delay', 5e-6), f'Q{i}') for i in qubits],
                *[('X/2', f'Q{i}') for i in qubits],
                *[('-X/2', f'Q{i}') for i in qubits],
                ('Barrier', tuple(f'Q{i}' for i in qubits)),
                *[(('Measure', j), f'Q{i}') for j, i in enumerate(qubits)]
            ], [
                *[(('Delay', 5e-6), f'Q{i}') for i in qubits],
                *[('X/2', f'Q{i}') for i in qubits],
                *[('X/2', f'Q{i}') for i in qubits],
                ('Barrier', tuple(f'Q{i}' for i in qubits)),
                *[(('Measure', j), f'Q{i}') for j, i in enumerate(qubits)]
            ], ],
        },
    }


def AllXY6and16_alpha_without_constrains(qubits: list[int], delta: Optional[float] = None, st: Optional[float] = None, ed: Optional[float] = None,
                                         sweep_points: int = 41, repeat: int = 1, signal: str = 'raw') -> dict:
    """
    [f'Q{i}'] change drag.alpha and measure AllXY 6 and AllXY 16 to determin the `rfUnitary.params.alpha`

    Args:
        qubits (list[int]): the qubit id.
        delta (Optional[float], optional): span alpha coefficient, in the dimension 1. Defaults to None.
        st (Optional[float], optional): start alpha coefficient, in the dimension 1. Defaults to None.
        ed (Optional[float], optional): end alpha coefficient, in the dimension 1. Defaults to None.
        sweep_points (int, optional): sweep points. Defaults to 41.
        repeat (int, optional): repeat times. Defaults to 1.
        signal (str, optional): signal type. Defaults to 'raw'.

    Returns:
        dict: config.
    """

    sweep_list = generate_spanlist(
        center=1, delta=delta, st=st, ed=ed, sweep_points=2)
    base = [kernel.get(f'gate.rfUnitary.Q{i}.params.alpha') for i in qubits]

    return {
        'init': {
            'name': 'AllXY6and16_alpha',
            'qubits': qubits,
            'signal': signal,
            'scanner_name': 'AllXY6and16_alpha_without_constrains',
            'shots': round(repeat)*1024,
        },
        'setting': {
            'pre_setting': {},
            'compile_once': False,
            'circuit_type': 'cmds:qlispcmd',
            'circuit': [],
        },
        'constrains': [],
        'sweep_config': dict(
            list({
                f'Q{i}': {
                    'addr': f'gate.rfUnitary.Q{i}.params.alpha',
                } for i in qubits
            }.items())+list({
                'circuit': {
                    'addr': f'setting.circuit'
                }
            }.items())
        ),
        'sweep_setting': {
            'circuit': [[[
                *[('Y/2', f'Q{i}') for i in qubits],
                *[(('Delay', kernel.get(f'gate.rfUnitary.Q{i}.params.duration')[1][0]), f'Q{i}') for i in qubits],
                ('Barrier', tuple(f'Q{i}' for i in qubits)),
                *[(('Measure', j), f'Q{i}') for j, i in enumerate(qubits)],
            ], [
                *[('Y', f'Q{i}') for i in qubits],
                *[('Y/2', f'Q{i}') for i in qubits],
                ('Barrier', tuple(f'Q{i}' for i in qubits)),
                *[(('Measure', j), f'Q{i}') for j, i in enumerate(qubits)],
            ], ], ],
            tuple([
                *[f'Q{i}' for i in qubits],
            ]): [np.linspace(
                max(0, sweep_list[0]*base[j]), min(1,
                                                   sweep_list[1]*base[j]), sweep_points
            ) for j, i in enumerate(qubits)],
        },
        'plot': [
            ['Scale', 'a.u.'], ['Probability' if signal ==
                                'state' else 'Amplitude', 'a.u.'],
        ],
    }


def AllXY7and8_delta_without_constrains(qubits: list[int], delta: Optional[float] = None, st: Optional[float] = None, ed: Optional[float] = None,
                                        sweep_points: int = 41, repeat: int = 1, signal: str = 'raw') -> dict:
    """
    [f'Q{i}'] change drag.delta and measure AllXY 7 and AllXY 8 to determin the `rfUnitary.params.delta`

    Args:
        qubits (list[int]): the qubit id.
        delta (Optional[float], optional): span delta coefficient, in the dimension frequency, Hz. Defaults to None.
        st (Optional[float], optional): start delta coefficient, in the dimension frequency, Hz. Defaults to None.
        ed (Optional[float], optional): end delta coefficient, in the dimension frequency, Hz. Defaults to None.
        sweep_points (int, optional): sweep points. Defaults to 41.
        repeat (int, optional): repeat times. Defaults to 1.
        signal (str, optional): signal type. Defaults to 'raw'.

    Returns:
        dict: [description]
    """

    sweep_list = generate_spanlist(
        center=0, delta=delta, st=st, ed=ed, sweep_points=sweep_points)

    return {
        'init': {
            'name': 'AllXY7and8_delta',
            'qubits': qubits,
            'signal': signal,
            'scanner_name': 'AllXY7and8_delta_without_constrains',
            'shots': round(repeat)*1024,
        },
        'setting': {
            'pre_setting': {},
            'compile_once': False,
            'circuit_type': 'cmds:qlispcmd',
            'circuit': [],
        },
        'constrains': [],
        'sweep_config': dict(
            list({
                f'Q{i}': {
                    'addr': f'gate.rfUnitary.Q{i}.params.delta',
                } for i in qubits
            }.items())+list({
                'circuit': {
                    'addr': f'setting.circuit'
                }
            }.items())
        ),
        'sweep_setting': {
            'circuit': [[
                *[('X/2', f'Q{i}') for i in qubits],
                *[('Y/2', f'Q{i}') for i in qubits],
                ('Barrier', tuple(f'Q{i}' for i in qubits)),
                *[(('Measure', j), f'Q{i}') for j, i in enumerate(qubits)]
            ], [
                *[('Y/2', f'Q{i}') for i in qubits],
                *[('X/2', f'Q{i}') for i in qubits],
                ('Barrier', tuple(f'Q{i}' for i in qubits)),
                *[(('Measure', j), f'Q{i}') for j, i in enumerate(qubits)]
            ], ],
            tuple([
                f'Q{i}' for i in qubits
            ]): [
                sweep_list+kernel.get(f'gate.rfUnitary.Q{i}.params.delta') for i in qubits
            ],
        },
        'plot': [
            ['Delta', 'Hz'], ['Probability' if signal ==
                              'state' else 'Amplitude', 'a.u.'],
        ],
    }


def AllXY11and12_beta_without_constrains(qubits: list[int], delta: Optional[float] = None, st: Optional[float] = None, ed: Optional[float] = None,
                                         sweep_points: int = 41, repeat: int = 1, signal: str = 'raw') -> dict:
    """
    [f'Q{i}'] change drag.beta and measure AllXY 11 and AllXY 12 to determin the `rfUnitary.params.beta`

    Args:
        qubits (list[int]): the qubit id.
        delta (Optional[float], optional): span beta coefficient, in the dimension 1e-9. Defaults to None.
        st (Optional[float], optional): start beta coefficient, in the dimension 1e-9. Defaults to None.
        ed (Optional[float], optional): end beta coefficient, in the dimension 1e-9. Defaults to None.
        sweep_points (int, optional): sweep points. Defaults to 41.
        repeat (int, optional): repeat times. Defaults to 1.
        signal (str, optional): signal type. Defaults to 'raw'.

    Returns:
        dict: [description]
    """

    sweep_list = generate_spanlist(
        center=0, delta=delta, st=st, ed=ed, sweep_points=sweep_points)

    return {
        'init': {
            'name': 'AllXY11and12_beta',
            'qubits': qubits,
            'signal': signal,
            'scanner_name': 'AllXY11and12_beta_without_constrains',
            'shots': round(repeat)*1024,
        },
        'setting': {
            'pre_setting': {},
            'compile_once': False,
            'circuit_type': 'cmds:qlispcmd',
            'circuit': [],
        },
        'constrains': [],
        'sweep_config': dict(
            list({
                f'Q{i}': {
                    'addr': f'gate.rfUnitary.Q{i}.params.beta',
                } for i in qubits
            }.items())+list({
                'circuit': {
                    'addr': f'setting.circuit'
                }
            }.items())
        ),
        'sweep_setting': {
            'circuit': [[
                *[('X', f'Q{i}') for i in qubits],
                *[('Y/2', f'Q{i}') for i in qubits],
                ('Barrier', tuple(f'Q{i}' for i in qubits)),
                *[(('Measure', j), f'Q{i}') for j, i in enumerate(qubits)],
            ], [
                *[('Y', f'Q{i}') for i in qubits],
                *[('X/2', f'Q{i}') for i in qubits],
                ('Barrier', tuple(f'Q{i}' for i in qubits)),
                *[(('Measure', j), f'Q{i}') for j, i in enumerate(qubits)],
            ], ],
            tuple([
                *[f'Q{i}' for i in qubits],
            ]): [
                sweep_list+kernel.get(f'gate.rfUnitary.Q{i}.params.beta') for i in qubits
            ],
        },
        'plot': [
            ['Beta', 'a.u.'], ['Probability' if signal ==
                               'state' else 'Amplitude', 'a.u.'],
        ],
    }


def ReadoutDelay_without_constrains(qubits: list[int], time_length: float, sweep_points: int = 41, signal: str = 'raw') -> dict:
    """
    ['time'] readout delay.

    Args:
        qubits (list[int]): the qubit id.
        time_length (float): delay time range, (-time_length, time_length) is applied.
        sweep_points (int, optional): sweep points. Defaults to 41.
        signal (str, optional): signal type. Defaults to 'raw'.

    Returns:
        dict: config.
    """

    assert time_length > 0, 'time_length should be positive.'

    delay_addition = {kernel.get(f'Q{i}.probe'): 0 for i in qubits}
    for j, i in enumerate(qubits):
        delay_addition[kernel.get(f'Q{i}.probe')] = max(delay_addition[kernel.get(
            f'Q{i}.probe')], kernel.get(f'gate.rfUnitary.Q{i}.params.duration')[1][-1])

    for j, i in enumerate(qubits):
        delay_addition[i] = delay_addition[kernel.get(
            f'Q{i}.probe')]-kernel.get(f'gate.rfUnitary.Q{i}.params.duration')[1][-1]

    return {
        'init': {
            'name': 'ReadoutDelay',
            'qubits': qubits,
            'signal': signal,
            'scanner_name': 'ReadoutDelay_without_constrains',
        },
        'setting': {
            'pre_setting': {},
            'compile_once': False,
            'circuit_type': 'cmds:qlispcmd',
            'circuit': [],
        },
        'constrains': [],
        'sweep_config': {
            'time': {
                'addr': None,
            },
            'circuit': {
                'addr': 'setting.circuit',
            },
        },
        'sweep_setting': {
            'time': np.linspace(-time_length, time_length, sweep_points),
        },
        'sweep_addition': {
            'circuit': lambda time: [
                *[(('Delay', time_length+delay_addition[i]),
                   f'Q{i}') for i in qubits],
                *[(('rfUnitary', np.pi, 0), f'Q{i}') for i in qubits],
                *[(('Delay', time), f'Q{i}') for i in qubits],
                ('Barrier', tuple(f'Q{i}' for i in qubits)),
                *[(('Measure', j), f'Q{i}') for j, i in enumerate(qubits)],
            ],
        },
        'plot': [
            ['Readout Delay', 's'], ['Probability' if signal ==
                                     'state' else 'Amplitude', 'a.u.'],
        ],
    }


def RTO_without_constrains(qubits: list[int], time_length: float, sweep_points: int = 5, signal: str = 'raw') -> dict:
    """
    [2, 'time'] In Ramsey experiment, x-axis projection and y-axis projection are measured replaced phase.

    Args:
        qubits (list[int]): the qubit id.
        time_length (float): length of delay time.
        sweep_points (int, optional): sweep points. Defaults to 5.
        signal (str, optional): signal type. Defaults to 'raw'.

    Returns:
        dict: config.
    """

    sweep_list = np.arange(0, time_length, time_length/sweep_points)

    return {
        'init': {
            'name': 'RTO',
            'qubits': qubits,
            'signal': signal,
            'scanner_name': 'RTO_without_constrains',
        },
        'setting': {
            'pre_setting': {},
            'compile_once': False,
            'circuit_type': 'cmds:qlispcmd',
            'circuit': [],
        },
        'constrains': [],
        'sweep_config': {
            'time': {
                'addr': None,
            },
            'circuit': {
                'addr': 'setting.circuit',
            },
            'gate': {
                'addr': None,
            },
        },
        'sweep_setting': {
            'gate': ['X/2', 'Y/2'],
            'time': sweep_list,
        },
        'sweep_addition': {
            'circuit': lambda time, gate: [
                *[('X/2', f'Q{i}') for i in qubits],
                *[(('Delay', time), f'Q{i}') for i in qubits],
                *[(gate, f'Q{i}') for i in qubits],
                ('Barrier', tuple(f'Q{i}' for i in qubits)),
                *[(('Measure', j), f'Q{i}') for j, i in enumerate(qubits)]
            ],
        },
        'plot': [
            ['Delay', 's'], ['Probability' if signal ==
                             'state' else 'Amplitude', 'a.u.'],
        ],
    }


def PiErrorOscillation_without_constrain(qubits: list[int], errorRate: float = 0.1, periods: int = 1, step: int = 1, signal: str = 'raw') -> dict:
    """
    ['count'] Multiply a known error on pi pulse to calibrate the error.

    Args:
        qubits (list[int]): the qubit id.
        errorRate (float, optional): error rate act on rfUnitary drive. Defaults to 0.1.
        periods (int, optional): number of period to measure. Defaults to 1.
        step (int, optional): 2*step size. Defaults to 1.
        signal (str, optional): signal type. Defaults to 'raw'.

    Returns:
        dict: config.
    """

    sweep_list = np.round(np.concatenate(
        (np.array([0]), np.arange(1, round(periods/errorRate), 2*step))))

    return {
        'init': {
            'name': 'PiErrorOscillation',
            'qubits': qubits,
            'signal': signal,
            'scanner_name': 'PiErrorOscillation_without_constrain',
        },
        'setting': {
            'pre_setting': {
                f'gate.rfUnitary.Q{i}.params.amp': [[0, 1], [0, (1-errorRate)*kernel.get(f'gate.rfUnitary.Q{i}.params.amp')[1][-1]]] for i in qubits
            },
            'compile_once': False,
            'circuit_type': 'cmds:qlispcmd',
            'circuit': [],
        },
        'constrains': [],
        'sweep_config': {
            'circuit': {
                'addr': 'setting.circuit',
            },
            'count': {
                'addr': None,
            },
        },
        'sweep_setting': {
            'count': sweep_list,
        },
        'sweep_addition': {
            'circuit': lambda count: [
                *[(('rfUnitary', np.pi, 0), f'Q{i}') for i in qubits]*count,
                ('Barrier', tuple(f'Q{i}' for i in qubits)),
                *[(('Measure', j), f'Q{i}') for j, i in enumerate(qubits)]
            ],
        },
        'plot': [
            ['Delay', 's'], ['Probability' if signal ==
                             'state' else 'Amplitude', 'a.u.'],
        ],
    }


def DRAGCheck_without_constrain(qubits: list[int], repeat: int = 1, signal: str = 'raw') -> dict:
    return {
        'init': {
            'name': 'DRAGCheck',
            'qubits': qubits,
            'signal': signal,
            'scanner_name': 'DRAGCheck_without_constrain',
            'shots': round(repeat)*1024,
        },
        'setting': {
            'pre_setting': {},
            'compile_once': False,
            'circuit_type': 'cmds:qlispcmd',
            'circuit': [],
        },
        'constrains': [],
        'sweep_config': {
            'circuit': {
                'addr': f'setting.circuit',
            },
        },
        'sweep_setting': {
            'circuit': [[
                *[(('Measure', j), f'Q{i}') for j, i in enumerate(qubits)],
            ], [
                *[('X', f'Q{i}') for i in qubits],
                *[('Y/2', f'Q{i}') for i in qubits],
                *[(('Measure', j), f'Q{i}') for j, i in enumerate(qubits)],
            ], [
                *[('Y', f'Q{i}') for i in qubits],
                *[('X/2', f'Q{i}') for i in qubits],
                *[(('Measure', j), f'Q{i}') for j, i in enumerate(qubits)],
            ], [
                *[('X', f'Q{i}') for i in qubits],
                *[(('Measure', j), f'Q{i}') for j, i in enumerate(qubits)],
            ], ],
        },
        'plot': [
            ['DRAG Scale', 'a.u.'], ['Probability' if signal ==
                                     'state' else 'Amplitude', 'a.u.'],
        ],
    }


def RB_single_qubit_without_constrain(qubits: list[int], rb_qubits: Optional[list[int]] = None, repeat: int = 1, signal: str = 'state',
                                      max_cycle: int = 500, base: Optional[list[list[tuple]]] = None, random_times: int = 20, start: int = 0,
                                      interleaves: Optional[list[str]] = None, sweep_points: int = 21) -> dict:
    """
    [None] RB on single qubit

    Args:
        qubits (list[int]): the readout qubit id
        rb_qubits (Optional[list[int]], optional): the qubit id which are acted on RB circuit. Defaults to None.
        repeat (int, optional): repeat times. Defaults to 1.
        signal (str, optional): signal type. Defaults to 'state'.
        max_cycle (int, optional): max cycle number. Defaults to 500.
        base (Optional[list[list[tuple]]], optional): base use. Defaults to None.
        random_times (int, optional): number of random times. Defaults to 20.
        interleaves (list[str], optional): interleaves gate. Defaults to [].
        sweep_points (int, optional): sweep points. Defaults to 21.

    Returns:
        dict: config.
    """

    from waveforms.quantum.rb import generateRBCircuit

    if rb_qubits is None:
        rb_qubits = qubits

    if interleaves is None:
        interleaves = []
    else:
        interleaves = [(interleave, 0) for interleave in interleaves]

    return {
        'init': {
            'name': 'RB_single_qubit',
            'qubits': qubits,
            'signal': signal,
            'scanner_name': 'RB_single_qubit_without_constrain',
            'shots': round(repeat)*1024,
        },
        'setting': {
            'pre_setting': {},
            'compile_once': False,
            'circuit_type': 'cmds:qlispcmd',
            'circuit': [],
        },
        'constrains': [],
        'sweep_config': {
            'circuit': {
                'addr': 'setting.circuit',
            },
            'cycle': {
                'addr': None,
            },
            'random_times': {
                'addr': None,
            }
        },
        'sweep_setting': {
            'random_times': np.arange(random_times),
            'cycle': generate_RB_cycle(max_cycle=max_cycle, sweep_points=sweep_points, start=start),
        },
        'sweep_addition': {
            'circuit': lambda cycle: [
                *[('X', f'Q{i}') for i in rb_qubits],
                *chain.from_iterable(generateRBCircuit(qubits=(f'Q{i}',), cycle=cycle,
                                                       seed=np.random.randint(0xfffffff), interleaves=interleaves, base=base) for i in rb_qubits),
                ('Barrier', tuple(f'Q{i}' for i in qubits)),
                *[(('Measure', j), f'Q{i}') for j, i in enumerate(qubits)],
            ],
        },
        'plot': [
            ['Count', 'a.u.'], ['Probability', 'a.u.'],
        ],
    }


def nop(qubits: list[int]) -> dict:
    """
    A null scanner.

    Args:
        qubits (list[int]): the qubit id

    Returns:
        dict: config.
    """

    return {
        'init': {
            'name': 'nop',
            'qubits': qubits,
            'scanner_name': 'nop',
        },
        'setting': {
            'pre_setting': {},
            'compile_once': False,
            'circuit_type': 'cmds:qlispcmd',
            'circuit': [],
        },
        'constrains': [],
        'sweep_config': {},
        'sweep_setting': {},
        'plot': [],
    }


def XEB_single_qubit_without_constrain(qubits: list[int], xeb_qubits: Optional[list[int]] = None, repeat: int = 1, signal: str = 'count', max_cycle: int = 40,
                                       random_times: int = 20, sweep_points: int = 21, start: float = 1) -> dict:
    """
    ['random_seed'] XEB on single qubit

    Args:
        qubits (list[int]): the readout qubit id
        xeb_qubits (Optional[list[int]], optional): the qubit id which are acted on XEB circuit. Defaults to None.
        repeat (int, optional): repeat times. Defaults to 1.
        signal (str, optional): signal type. Defaults to 'state'.
        max_cycle (int, optional): max cycle number. Defaults to 500.
        random_times (int, optional): number of random times. Defaults to 20.
        sweep_points (int, optional): sweep points. Defaults to 21.
        start (float, optional): 10^start to start in this measure to aviod too few cycles.

    Returns:
        dict: config.
    """

    from waveforms.quantum.xeb import generateXEBCircuit

    if xeb_qubits is None:
        xeb_qubits = qubits

    return {
        'init': {
            'name': 'XEB_single_qubit',
            'qubits': qubits,
            'signal': signal,
            'scanner_name': 'XEB_single_qubit_without_constrain',
            'shots': round(repeat)*1024,
        },
        'setting': {
            'pre_setting': {},
            'compile_once': False,
            'circuit_type': 'cmds:qlispcmd',
            'circuit': [],
        },
        'constrains': [],
        'sweep_config': {
            'circuit': {
                'addr': 'setting.circuit',
            },
            'cycle': {
                'addr': None,
            },
            'random_seed': {
                'addr': None,
            }
        },
        'sweep_setting': {
            'cycle': generate_RB_cycle(max_cycle=max_cycle, sweep_points=sweep_points, start=start),
            'random_seed': np.random.randint(0xfffffff, size=[random_times, ]),
        },
        'sweep_addition': {
            'circuit': lambda cycle, random_seed: [
                *generateXEBCircuit(qubits=xeb_qubits,
                                    cycle=cycle, seed=random_seed, mode='s'),
                ('Barrier', tuple(f'Q{i}' for i in qubits)),
                *[(('Measure', j), f'Q{i}') for j, i in enumerate(qubits)],
            ],
        },
        'plot': [
            ['Count', 'a.u.'], ['Probability', 'a.u.'],
        ],
    }


def XXDelta_without_constrain(qubits: list[int], n: int = 1, bound: float = 60e6, signal: str = 'state', sweep_points: int = 21, mode: str = 'linear') -> dict:
    """
    [f'Q{i}'] measure DRAG delta using a sequence as 'Y'-'X'-'-X'-'X'-'-X'-...-'X'-'-X'.

    Args:
        qubits (list[int]): the qubit id.
        n (int, optional): numbers of pulses 'X' and '-X'. Defaults to 1.
        bound (float, optional): delta upper bound, actually bound/n is applied. Defaults to 60e6.
        signal (str, optional): signal type. Defaults to 'state'.
        sweep_points (int, optional): sweep points. Defaults to 21.
        mode (str, optional): in ['linear' (for linear time sampling), 'log' (for log time sampling)]. Defaults to 'linear'.

    Returns:
        dict: config.
    """

    if mode == 'linear':
        sweep_list = generate_spanlist(center=0, delta=bound/n, sweep_points=sweep_points)
    elif mode == 'log':
        sweep_list = generate_spanlist_log(center=0, delta=bound/n, sweep_points=sweep_points)
    else:
        raise ValueError(f'Mode {mode} is not supported.')

    return {
        'init': {
            'name': 'X-XDelta',
            'qubits': qubits,
            'signal': signal,
            'scanner_name': 'XXDelta_without_constrain',
        },
        'setting': {
            'pre_setting': {},
            'compile_once': False,
            'circuit_type':
            'cmds:qlispcmd',
            'circuit': [
                *[(('rfUnitary', np.pi, np.pi/2), f'Q{i}') for i in qubits],
                *chain.from_iterable(zip([*[(('rfUnitary', np.pi, 0), f'Q{i}') for i in qubits] * n],
                                         [
                    *[(('rfUnitary', np.pi, np.pi), f'Q{i}')
                      for i in qubits] * n
                ])),
                ('Barrier', tuple(f'Q{i}' for i in qubits)),
                *[(('Measure', j), f'Q{i}') for j, i in enumerate(qubits)],
            ]
        },
        'constrains': [],
        'sweep_config': {
            f'Q{i}': {
                'addr': f'gate.rfUnitary.Q{i}.params.delta',
            } for i in qubits
        },
        'sweep_setting': {
            tuple([f'Q{i}' for i in qubits]): [
                sweep_list+kernel.get(f'gate.rfUnitary.Q{i}.params.delta') for i in qubits
            ],
        },
    }

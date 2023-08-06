# Rebuild: Liu Pei  <liupei200546@163.com>  2022/03/29

import numpy as np
from itertools import chain
import kernel

from typing import Optional

from .tools import generate_log_intlist

__all__ = [
    'Count_n', 'AllXY_without_constrains',
    'RB_single_qubit',
    'RB_two_qubits', 'RB_two_qubits_IBM',
    'QPT_two_qubits'
]


def Count_n(qubits: list[str],
            max_n: int = 100, step_n: float = 10,
            signal: str = 'iq_avg', act_qubits: Optional[list[str]] = None, **kw) -> dict:
    """
    ['n'] Count of X gate.

    Args:
        qubits (list[str]): qubit names.
        max_n (int, optional): maximum of n. Defaults to 100.
        step_n (float, optional): step of n. Defaults to 10.
        signal (str, optional): signal. Defaults to 'iq_avg'.
        act_qubits (Optional[list[str]], optional): act qubits. Defaults to None.
    """

    act_qubits = qubits if act_qubits is None else act_qubits

    return {
        'init': {
            'name': 'N Count',
            'qubits': qubits,
            'signal': signal,
        },
        'sweep_setting': {
            'n': np.arange(step_n, max_n+1, step_n),
        },
        'sweep_addition': {
            'circuit': lambda n: [
                *[(('rfUnitary', np.pi, 0), q) for q in act_qubits]*n,
                ('Barrier', tuple(qubits)),
                *[(('Measure', j), q) for j, q in enumerate(qubits)],
            ],
        },
    }


def AllXY_without_constrains(qubits: list[str],
                             n: int = 0, repeat: int = 1,
                             signal: str = 'population', act_qubits: Optional[list[str]] = None, **kw) -> dict:
    """
    [21] AllXY 21 circuit.

    Args:
        qubits (list[str]): qubit names.
        n (int, optional): repeat of gate. Defaults to 0.
        repeat (int, optional): repeat times. Defaults to 1.
        signal (str, optional): signal. Defaults to 'population'.
        act_qubits (Optional[list[str]], optional): act qubits. Defaults to None.
    """

    def _changeI(q):
        params = kernel.get(f'gate.rfUnitary.{q}.params')
        return params.get('duration', [[0, 0.5], [0, 0]])[-1][-1]+params.get('buffer', 0)

    def _span_n(x, n, changeI: float = None):
        if n == 0:
            return x
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

    from waveforms.quantum import ALLXY

    act_qubits = qubits if act_qubits is None else act_qubits
    rfUnitary_time = {q: _changeI(q) for q in act_qubits}

    return {
        'init': {
            'name': 'All XY',
            'qubits': qubits,
            'signal': signal,
        },
        'sweep_setting': {
            'number': np.arange(21),
            'repeat': np.arange(repeat),
        },
        'sweep_addition': {
            'circuit': lambda number: [
                *chain.from_iterable(_span_n(ALLXY(qubit=q, i=number), n,
                                             rfUnitary_time[q]) for q in act_qubits),
                ('Barrier', tuple(qubits)),
                *[(('Measure', j), q) for j, q in enumerate(qubits)],
            ],
        },
    }


def RB_single_qubit(qubits: list[str],
                    start: int = 1, max_cycle: int = 500, sweep_points: int = 21,
                    random_times: int = 20,
                    base: Optional[list[list[tuple]]] = None, interleaves: list = [[]],
                    ini_gate: list = ['X'],
                    signal: str = 'population', act_qubits: Optional[list[str]] = None, **kw) -> dict:
    """
    ['seed'] RB on single qubit.

    Args:
        qubits (list[str]): qubit names.
        start (int, optional): start number. Defaults to 1.
        max_cycle (int, optional): maximum of cycle. Defaults to 500.
        sweep_points (int, optional): sweep points. Defaults to 21.
        random_times (int, optional): random times. Defaults to 20.
        base (Optional[list[list[tuple]]], optional): RB base. Defaults to None.
        interleaves (list): interleaves gate. Defaults to [].
        ini_gate (list): initial gate. Defaults to ['X'].
        signal (str, optional): signal. Defaults to 'population'.
        act_qubits (Optional[list[str]], optional): act qubits. Defaults to None.
    """

    from waveforms.quantum.rb import generateRBCircuit

    act_qubits = qubits if act_qubits is None else act_qubits

    ret = {
        'init': {
            'name': 'RB Single Qubit',
            'qubits': qubits,
            'signal': signal,
        },
        'sweep_setting': {
            'seed': [np.random.randint(0xfffffff) for _ in range(random_times)],
            'cycle': generate_log_intlist(min_int=start, max_int=max_cycle, sweep_points=sweep_points),
        },
        'sweep_addition': {
            'circuit': lambda cycle, seed, interleave_id=0, interleaves=interleaves: [
                *[(gate, q) for gate in ini_gate for q in act_qubits],
                *chain.from_iterable(generateRBCircuit(qubits=(q,), cycle=cycle,
                                                       seed=seed, interleaves=interleaves[interleave_id], base=base) for q in act_qubits),
                ('Barrier', tuple(qubits)),
                *[(('Measure', j), q) for j, q in enumerate(qubits)],
            ],
        },
    }
    
    if len(interleaves):
        ret['sweep_setting']['interleave_id'] = np.arange(len(interleaves))

    return ret


def RB_two_qubits(qubits: list[tuple[str]],
                  start: int = 1, max_cycle: int = 50, sweep_points: int = 21,
                  random_times: int = 20,
                  base: Optional[list[list[tuple]]] = None, interleaves: list = [[]],
                  ini_gate: list = [('X', 'X')],
                  signal: str = 'diag', act_qubits: Optional[list[tuple[str]]] = None, **kw) -> dict:
    """
    ['seed'] RB on two qubit.

    Args:
        qubits (list[tuple[str]]): qubit names.
        start (int, optional): start number. Defaults to 1.
        max_cycle (int, optional): maximum of cycle. Defaults to 500.
        sweep_points (int, optional): sweep points. Defaults to 21.
        random_times (int, optional): random times. Defaults to 20.
        base (Optional[list[list[tuple]]], optional): RB base. Defaults to None.
        interleaves (list): interleaves gate. Defaults to [].
        ini_gate (list, optional): initial gate. Defaults to [('X', 'X')].
        signal (str, optional): signal. Defaults to 'diag'.
        act_qubits (Optional[list[str]], optional): act qubits. Defaults to None.
    """

    act_qubits = qubits if act_qubits is None else act_qubits
    from waveforms.quantum.rb import generateRBCircuit

    ret = {
        'init': {
            'name': 'RB Two Qubits',
            'qubits': qubits,
            'signal': signal,
        },
        'sweep_setting': {
            'seed': np.random.randint(0xfffffff, size=[random_times]),
            'cycle': generate_log_intlist(min_int=start, max_int=max_cycle, sweep_points=sweep_points),
        },
        'sweep_addition': {
            'circuit': lambda cycle, seed, interleave_id=0, interleaves=interleaves: [
                *[(gate[i], q[i]) for i in range(2)
                  for gate in ini_gate for q in act_qubits],
                *chain.from_iterable(generateRBCircuit(qubits=q, cycle=cycle, interleaves=interleaves[interleave_id],
                                                       seed=seed, base=base) for q in act_qubits),
                ('Barrier', tuple(chain.from_iterable(qubits))),
                *[(('Measure', i), q) for i, q in enumerate(chain(*qubits))],
            ],
        },
    }

    if len(interleaves):
        ret['sweep_setting']['interleave_id'] = np.arange(len(interleaves))
    
    return ret


def _cr_2RB(qubits, cycle, seed, base, interleaves):

    from waveforms.quantum.clifford.clifford import inv, mul
    import random
    # from waveforms.quantum.rb import replace_qubit, index_to_circuit
    from waveforms.quantum.rb import index_to_circuit
    from waveforms.qlisp import mapping_qubits

    assert len(qubits) == 2, 'Invalid qubits length'

    MAX = 24*24

    ret = []
    index = 0
    rng = random.Random(seed)
    int_id, int_gate = interleaves

    for _ in range(cycle):
        i = rng.randrange(MAX)
        ret.extend(index_to_circuit(i, qubits, base, rng))
        index = mul(i, index)
        ret.extend(int_gate)
        index = mul(int_id, index)

    ret.extend(index_to_circuit(inv(index), qubits, base, rng))

    mapping = {i: q for i, q in enumerate(qubits)}

    # return replace_qubit(ret, qubits)
    return mapping_qubits(ret, mapping)


def RB_two_qubits_IBM(qubits: list[tuple[str]],
                      start: int = 1, max_cycle: int = 50, sweep_points: int = 21,
                      random_times: int = 20,
                      base: Optional[list[list[tuple]]] = None,
                      ini_gate: list = [('X', 'X')], gate_list=[(576, [('Cnot', (0, 1))])],
                      signal: str = 'diag', act_qubits: Optional[list[tuple[str]]] = None, **kw) -> dict:
    """_summary_

    Args:
        qubits (list[tuple[str]]): qubit names.
        start (int, optional): start number. Defaults to 1.
        max_cycle (int, optional): maximum of cycle. Defaults to 500.
        sweep_points (int, optional): sweep points. Defaults to 21.
        random_times (int, optional): random times. Defaults to 20.
        base (Optional[list[list[tuple]]], optional): RB base. Defaults to None.
        ini_gate (list, optional): initial gate. Defaults to [('X', 'X')].
        gate_list (list, optional): insert gates [(num in base, circuit form)]. Defaults to [(576, [('Cnot', (0, 1))])].
        signal (str, optional): signal. Defaults to 'diag'.
        act_qubits (Optional[list[str]], optional): act qubits. Defaults to None.
    """

    act_qubits = qubits if act_qubits is None else act_qubits

    return {
        'init': {
            'name': 'RB Two Qubits IBM',
            'qubits': qubits,
            'signal': signal,
        },
        'sweep_setting': {
            'gate': gate_list,
            'seed': np.random.randint(0xfffffff, size=[random_times]),
            'cycle': generate_log_intlist(max_int=max_cycle, sweep_points=sweep_points, min_int=start),
        },
        'sweep_addition': {
            'circuit': lambda gate, cycle, seed: [
                *[(gate[i], q[i]) for i in range(2)
                  for gate in ini_gate for q in act_qubits],
                *chain.from_iterable(_cr_2RB(qubits=q, cycle=cycle, interleaves=gate,
                                             seed=seed, base=base) for q in act_qubits),
                ('Barrier', tuple(chain.from_iterable(qubits))),
                *[(('Measure', i), q) for i, q in enumerate(chain(*qubits))],
            ],
        },
    }


def QPT_two_qubits(qubits: list[tuple[str]], process: list,
                   signal: str = 'diag', **kw) -> dict:
    """
    [None] Quantum process tomography

    Args:
        qubits (list[tuple[str]]): qubit names.
        process (list): process.
        signal (str, optional): signal. Defaults to 'diag'.
    """

    from waveforms.quantum.tomo import qstOpList, qptInitList
    from waveforms.quantum.rb import mapping_qubits

    return {
        'init': {
            'name': 'QPT',
            'qubits': qubits,
            'signal': signal,
        },
        'sweep_setting': {
            'ini': list(qptInitList(2)),
            'qst': list(qstOpList(2)),
        },
        'sweep_addition': {
            'circuit': lambda ini, qst, process=process: [
                *[(ini[0], q[0]) for q in qubits],
                *[(ini[1], q[1]) for q in qubits],
                *chain.from_iterable(mapping_qubits(process, {ii:qq for ii, qq in enumerate(q)})
                                     for q in qubits),
                *[(qst[i], q[i]) for i in range(2) for q in qubits],
                ('Barrier', tuple(chain.from_iterable(qubits))),
                *[(('Measure', j), q)
                  for j, q in enumerate(chain.from_iterable(qubits))],
            ],
        },
    }

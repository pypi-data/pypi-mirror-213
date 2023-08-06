# Rebuild & Author: Liu Pei <liupei200546@163.com>  2021/08/14


from typing import Union

import numpy as np
from qos_tools.analyzer.tools import get_rotate_phi


def generate_1D_mean(result: dict, index: list[str], shape: list, sig: str, state_limit: int) -> list[dict]:
    assert sig in ['data', 'states']
    for j, i in enumerate(index):
        ret = {
            'x': np.asarray(result['index'][index[j]][:shape[0]]),
            'y': np.mean(result[sig][:, :, j], axis=-1).reshape(shape),
        }
        if sig=='states':
            count = result['states'][:, :, j]
            population = []
            for state in range(state_limit):
                population.append(np.mean(np.where(count==state, 1, 0), axis=-1).reshape(shape))
            ret['population'] = np.asarray(population)
            ret['y'] = population[1]
        yield ret


def format_conversion(scanner: str, result: dict, qubits: list[Union[int, tuple]], signal: str = 'raw', state_limit: int = 2) -> list[dict]:

    sig = 'states' if signal == 'state' else 'data'

    if scanner in [
        'S21_base_change_lo_with_constrains'
    ]:
        ret = []
        for item in generate_1D_mean(state_limit=state_limit, result=result, index=['delta' for _ in qubits], shape=[result[sig].shape[0], ], sig=sig):
            item['y'] = np.abs(item['y'])
            ret.append(item)
        return ret

    elif scanner in [
        'S21_base_change_lo_without_constrains',
        'S21_base_change_awg',
        'S21_change_lo_without_constrains',
    ]:
        ret = []
        for item in generate_1D_mean(state_limit=state_limit, result=result, index=[f'Q{i}' for i in qubits], shape=[result[sig].shape[0], ], sig=sig):
            item['y'] = np.abs(item['y'])
            ret.append(item)
        return ret

    elif scanner in [
        'Spectrum_base_change_awg_without_constrains',
        'Spectrum_base_change_lo_without_constrains',
    ]:
        ret = []
        for item in generate_1D_mean(state_limit=state_limit, result=result, index=[f'Q{i}' for i in qubits], shape=[result[sig].shape[0], ], sig=sig):
            item['y'] = np.abs(get_rotate_phi(item['y']-np.mean(item['y'])))
            ret.append(item)
        return ret

    elif scanner in [
        'PowerRabi_base_scaleTimes',
        'PowerRabi_base_n_pulse',
        'TimeRabi_base_durationTimes',
        'XXDelta_without_constrain'
    ]:
        ret = []
        for item in generate_1D_mean(state_limit=state_limit, result=result, index=[f'Q{i}' for i in qubits], shape=[result[sig].shape[0], ], sig=sig):
            if signal == 'raw':
                item['y'] = np.real(get_rotate_phi(item['y']-item['y'][0]))
            ret.append(item)
        return ret

    elif scanner in [
        'T1_without_constrains'
    ]:
        ret = []
        for item in generate_1D_mean(state_limit=state_limit, result=result, index=[f'Q{i}' for i in qubits], shape=[result[sig].shape[0], ], sig=sig):
            if signal == 'raw':
                item['y'] = np.real(get_rotate_phi(item['y']-item['y'][-1]))
            ret.append(item)
        return ret

    elif scanner in [
        'Ramsey_without_constrains',
        'SpinEcho_without_constrains',
        'CPMG_without_constrains',
        'CP_without_constrains',
        'ReadoutDelay_without_constrains',
        'RTO_without_constrains'
    ]:
        ret = []
        for item in generate_1D_mean(state_limit=state_limit, result=result, index=['time' for _ in qubits], shape=[result[sig].shape[0], ], sig=sig):
            if signal == 'raw':
                item['y'] = np.real(get_rotate_phi(item['y']-item['y'][0]))
            ret.append(item)
        return ret

    elif scanner in [
        'ReadoutFrequency_without_constrains',
        'ReadoutAmp_without_constrains',
    ]:
        ret = []
        lth = (result['data'].shape[0])//state_limit
        for j, i in enumerate(qubits):
            ret.append({
                'x': np.asarray(result['index'][f'Q{i}'])[:lth],
            })
            for cur_state in range(state_limit):
                ret[-1][f'S{cur_state}'] = result[sig][cur_state*lth:cur_state*lth+lth, :, j]
        return ret

    elif scanner in [
        'Scatter2',
        'Scatter3',
    ]:
        ret = []
        for j, i in enumerate(qubits):
            ret.append({})
            for cur_state in range(state_limit):
                ret[-1][f'S{cur_state}'] = result[sig][cur_state, :, j]
        return ret

    elif scanner in [
        'AllXY_without_constrains',
        'DRAGCheck_without_constrain'
    ]:
        ret = []
        for j, i in enumerate(qubits):
            item = {'y': np.mean(result[sig][:, :, j], axis=-1)}
            if signal == 'raw':
                item['y'] = np.real(get_rotate_phi(item['y']-item['y'][0]))
            else:
                count = result['states'][:, :, j]
                population = []
                for state in range(state_limit):
                    population.append(np.mean(np.where(count==state, 1, 0), axis=-1))
                item['population'] = np.asarray(population)
                item['y'] = population[1]
            ret.append(item)
        return ret
    elif scanner in [
        'AllXY6and16_alpha_without_constrains',
        'AllXY7and8_delta_without_constrains',
        'AllXY11and12_beta_without_constrains',
    ]:
        ret = []
        for j, i in enumerate(qubits):
            x = np.asarray(result['index'][f'Q{i}'])
            y = np.mean(result[sig][:, :, j], axis=-1)
            ret.append({
                'x': x[:y.shape[0]//2],
            })
            if signal == 'raw':
                y = np.real(get_rotate_phi(y))
            else:
                count = result['states'][:, :, j]
                population = []
                for state in range(state_limit):
                    population.append(np.mean(np.where(count==state, 1, 0), axis=-1).reshape([y.shape[0]//2, 2]))
                ret[-1]['population'] = np.asarray(population)
                ret[-1]['y'] = population[1]
            ret[-1]['y1'] = y[:y.shape[0]//2],
            ret[-1]['y2'] = y[y.shape[0]//2:],
        return ret
    elif scanner in [
        'PiErrorOscillation_without_constrain',
    ]:
        ret = []
        for item in generate_1D_mean(state_limit=state_limit, result=result, index=['count' for _ in qubits], shape=[result[sig].shape[0], ], sig=sig):
            if signal == 'raw':
                item['y'] = np.real(get_rotate_phi(item['y']-item['y'][0]))
            ret.append(item)
        return ret

    elif scanner in [
        'RB_single_qubit_without_constrain'
    ]:
        ret = []
        for j, i in enumerate(qubits):
            item = {'y': np.mean(result[sig][:, :, j], axis=-1)}
            if signal == 'raw':
                item['y'] = np.real(get_rotate_phi(item['y']))
            else:
                count = result['states'][:, :, j]
                population = []
                for state in range(state_limit):
                    population.append(np.mean(np.where(count==state, 1, 0), axis=-1))
                item['population'] = np.asarray(population)
                item['y'] = population[1]
            ret.append(item)
        return ret

    elif scanner in [
        'XEB_single_qubit_without_constrain'
    ]:
        assert signal == 'count', 'signal type is invalid.'

        cycle = list(set(result['index']['cycle']))
        seeds = list(set(result['index']['random_times']))

        return {
            'cycle': cycle,
            'seeds': seeds,
            'counts': result['counts'],
        }

    elif scanner in [
        'nop',
    ]:
        return [{} for _ in qubits]
    else:
        raise ValueError('scanner is not supported')

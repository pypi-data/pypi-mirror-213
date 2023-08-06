# Author: lizhiyuan  <lizhiyuan@baqis.ac.cn>  2021/01/01
# Priority algorithm support by Liupei

import numpy as np


def extract_align_info(stdgatemap):
    '''提取对齐位置信息字典'''
    align_info = {}
    for qubit, gatelist in stdgatemap.items():
        for i, stdindex in enumerate(gatelist):
            operator, qubits, params = stdindex
            if operator.count(':'):
                if operator not in align_info:
                    align_info[operator] = {}
                align_info[operator][qubit] = i
    return align_info


def extract_gateMap_priority(stdgatemap, align_info):
    '''计算gateMap_priority'''
    gateMap_priority = {
        qubit: np.array(range(len(gatelist)))
        for qubit, gatelist in stdgatemap.items()
    }

    for qubit in stdgatemap.keys():
        flt = filter((lambda v, q=qubit: q in v.keys()),
                     align_info.values())
        sort = sorted(flt, key=lambda v, q=qubit: v[q])
        for align_dct in sort:
            priority_max = max(gateMap_priority[qubit][idx]
                               for qubit, idx in align_dct.items())
            for qubit, idx in align_dct.items():
                p_add = priority_max - gateMap_priority[qubit][idx]
                gateMap_priority[qubit][idx:] += p_add
    return gateMap_priority


def extract_align_priority_dict(gateMap_priority, align_info):
    '''提取对齐标记的优先度列表'''
    align_priority_dict = {}
    for align_tag, dct in align_info.items():
        align_qubits = list(dct.keys())
        qubit, gindex = list(dct.items())[0]
        align_priority = gateMap_priority[qubit][gindex]
        align_priority_dict[align_priority] = align_qubits
    return align_priority_dict


def extract_priority_info(gateMap_priority):
    '''按照优先度分类，提取排版顺序信息'''
    priority_info = {}
    for qubit, prioritylist in gateMap_priority.items():
        for i, priority in enumerate(prioritylist):
            if priority not in priority_info:
                priority_info[priority] = []
            priority_info[priority].append((qubit, i))
    return priority_info


def extract_gate_info(stdgatemap, priority_info):
    cmds = []
    for priority in sorted(priority_info.keys()):
        _cmds = []
        _barr_qubit_list = []
        for q, i in priority_info[priority]:
            stdindex = stdgatemap[q][i]
            operator, qubits, params = stdindex
            if len(qubits) > 1:
                # 校验多比特门的对齐规范
                _stdindex = stdgatemap[q][i-1]
                _operator, _qubits, _params = _stdindex
                assert _operator.count(
                    ':'), f"Qubit '{q}' {i+1}-th gate '{stdindex}' miss alignment mark !!!"
                assert q in qubits, f"Qubit '{q}' not support '{stdindex}'!"
            elif len(qubits) == 1:
                assert qubits[0] == q, f"Qubit '{q}' {i+1}-th gate '{stdindex}' error!"
            else:
                qubits = (q,)

            if operator.count(':'):
                _barr_qubit_list.extend(qubits)
            else:
                _cmds.append((operator, qubits, params))

        # 取集合，消除重复的多比特门操作
        _cmds_set = set(_cmds)
        # 校验 ############################
        qubits_op = []
        for operator, qubits, params in _cmds_set:
            qubits_op.extend(qubits)
        assert len(_cmds) == len(qubits_op) == len(
            set(qubits_op)), f'part of multi-qubit gate missing!'
        # ############################
        cmds.extend(_cmds_set)

        if _barr_qubit_list:
            barr_cmd = ('Barrier', tuple(_barr_qubit_list), tuple())
            cmds.append(barr_cmd)
    return cmds

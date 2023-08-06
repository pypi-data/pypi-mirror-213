# Author: lizhiyuan  <lizhiyuan@baqis.ac.cn>  2021/08/08
from qos_tools.gatemap.__info_extract import extract_align_info, extract_gateMap_priority, extract_priority_info, extract_gate_info


def stdgatemap2stdcmds(stdgatemap):
    '''
    stdgatemap: 形如，
        {
            'Q1': ['X', 'X/2', ':1:', 'CZ(Q1,Q2)', 'I', 'Y', ':3:'],
            'Q2': ['-Y/2',':1:','CZ(Q1,Q2)',':4:','CZ(Q2,Q3)','I','Y',':3:',],
            'Q3': [':4:', 'CZ(Q2,Q3)', 'I', 'Y', ':3:', 'Y'],
        }
    stdcmds: 形如，
        [('-Y/2', ('Q2',), ()),
        ('X', ('Q1',), ()),
        ('X/2', ('Q1',), ()),
        ('Barrier', ('Q1', 'Q2'), ()),
        ('CZ', ('Q1', 'Q2'), ()),
        ('I', ('Q1',), ()),
        ('Barrier', ('Q2', 'Q3'), ()),
        ('CZ', ('Q2', 'Q3'), ()),
        ('Y', ('Q1',), ()),
        ('I', ('Q2',), ()),
        ('I', ('Q3',), ()),
        ('Y', ('Q3',), ()),
        ('Y', ('Q2',), ()),
        ('Barrier', ('Q1', 'Q2', 'Q3'), ()),
        ('Y', ('Q3',), ())]
    '''
    align_info = extract_align_info(stdgatemap)
    gateMap_priority = extract_gateMap_priority(stdgatemap, align_info)
    priority_info = extract_priority_info(gateMap_priority)
    stdcmds = extract_gate_info(stdgatemap, priority_info)
    return stdcmds


def stdcmds2stdgatemap(stdcmds):
    stdgatemap = {}
    count = 0
    for operator, qubits, params in stdcmds:
        for qubit in qubits:
            if qubit not in stdgatemap.keys():
                stdgatemap[qubit] = []

        if len(qubits) == 1:
            qubit, = qubits
            stdindex = (operator, (), params)
            stdgatemap[qubit].append(stdindex)
        else:
            if operator in ['Barrier']:
                stdindex = None
            else:
                stdindex = (operator, qubits, params)
            alignTag = (f'Barrier:{count}', tuple(), tuple())
            count += 1
            for qubit in qubits:
                stdgatemap[qubit].append(alignTag)
                if stdindex is not None:
                    stdgatemap[qubit].append(stdindex)
    return stdgatemap


def gatemap_convert(gatemap, fr='stdindex', to='tupindex'):
    from ._index_convert import index_convert
    res_gatemap = {}
    for q, gatelist in gatemap.items():
        if q not in res_gatemap.keys():
            res_gatemap[q] = []

        for index in gatelist:
            _index = index_convert(index, fr, to)
            res_gatemap[q].append(_index)
    return res_gatemap


def cmds_convert(cmds, fr='stdcmd', to='qlispcmd'):
    from ._cmd_convert import cmd_convert
    res_cmds = []
    for cmd in cmds:
        _cmd = cmd_convert(cmd, fr, to)
        res_cmds.append(_cmd)
    return res_cmds


def circuit_convert(circuit, fr='gatemap:tupindex', to='cmds:qlispcmd'):
    ''''''
    if fr != to:
        cir_type_fr, cmd_type_fr = fr.split(':')
        cir_type_to, cmd_type_to = to.split(':')

        cir_type_support = ['gatemap', 'cmds']
        assert cir_type_fr in cir_type_support, f"circuit tpye '{cir_type_fr}' not support!"
        assert cir_type_to in cir_type_support, f"circuit tpye '{cir_type_to}' not support!"

        cmd_type_support = ['strindex', 'tupindex', 'stdindex',
                            'stdcmd', 'qlispcmd']
        assert cmd_type_fr in cmd_type_support, f"cmd tpye '{cmd_type_fr}' not support!"
        assert cmd_type_to in cmd_type_support, f"cmd tpye '{cmd_type_to}' not support!"

        if cir_type_fr in ['gatemap']:
            circuit = gatemap_convert(circuit, cmd_type_fr, 'stdindex')
        elif cir_type_fr in ['cmds']:
            circuit = cmds_convert(circuit, cmd_type_fr, 'stdcmd')
        else:
            raise

        if cir_type_fr == cir_type_to:
            pass
        else:
            if cir_type_fr == 'gatemap' and cir_type_to == 'cmds':
                circuit = stdgatemap2stdcmds(circuit)
            elif cir_type_fr == 'cmds' and cir_type_to == 'gatemap':
                circuit = stdcmds2stdgatemap(circuit)
            else:
                raise

        if cir_type_to in ['gatemap']:
            circuit = gatemap_convert(circuit, 'stdindex', cmd_type_to)
        elif cir_type_to in ['cmds']:
            circuit = cmds_convert(circuit, 'stdcmd', cmd_type_to)
        else:
            raise
    return circuit

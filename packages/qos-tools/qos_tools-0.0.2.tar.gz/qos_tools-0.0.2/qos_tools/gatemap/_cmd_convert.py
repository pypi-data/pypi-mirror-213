# Author: lizhiyuan  <lizhiyuan@baqis.ac.cn>  2021/08/08

def qlispcmd2stdcmd(qlispcmd):
    '''
    qlispcmd: 
        ((operator, *params), qubits)
        (operator, qubits)
        (operator, qubit)
    stdcmd: 
        (operator,qubits,params)
    '''
    op_para, qubits = qlispcmd
    if isinstance(op_para, tuple):
        operator, *params = op_para
    else:
        operator = op_para
        params = tuple()
    if isinstance(qubits, str):
        qubits = (qubits,)
    stdcmd = (operator, qubits, params)
    return stdcmd


def stdcmd2qlispcmd(stdcmd):
    '''
    qlispcmd:
        ((operator, *params), qubits)
        (operator, qubits)
        (operator, qubit)

    stdcmd:
        (operator,qubits,params)
    '''

    operator, qubits, params = stdcmd
    if len(qubits) == 1:
        qubits, = qubits

    if params:
        qlispcmd = ((operator, *params), qubits)
    else:
        qlispcmd = (operator, qubits)
    return qlispcmd


def cmd_convert(cmd, fr='qlispcmd', to='stdcmd'):
    '''index转换的统一接口'''
    if fr != to:
        cov_dict = {
            ('qlispcmd', 'stdcmd'): ('qlispcmd', 'stdcmd'),
            ('stdcmd', 'qlispcmd'): ('stdcmd', 'qlispcmd'),

        }
        cov = cov_dict[(fr, to)]
        cov_funcs = (eval(f'{cov[i]}2{cov[i+1]}') for i in range(len(cov)-1))

        for cov_func in cov_funcs:
            cmd = cov_func(cmd)
    return cmd

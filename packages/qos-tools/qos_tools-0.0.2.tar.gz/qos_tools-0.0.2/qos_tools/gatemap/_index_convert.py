# Author: lizhiyuan  <lizhiyuan@baqis.ac.cn>  2021/01/01
import re


def _parser_header(header):
    pat = re.compile('(.+)\((.*)\)$')
    m = pat.search(header)
    if m:
        operator = (m.group(1))
        qubits = m.group(2).split(',')
    else:
        operator = header
        qubits = []
    return operator, tuple(qubits)


def strindex2stdindex(strindex):
    ''' strindex to stdindex
    Parameters:
        index: str, 
            以operator标志开头；
            如果是多比特门，则用小括号和逗号(xx,xx)表示；
            如果含参，则用下划线连接参数。
            例如，'X', 'U_0_180', 'iSwap(Q1,Q2)', 'CRz(Q1,Q2)_90'
    Return: stdindex,
        (operator, tuple(qubit), tuple(params))
    '''
    header, *params = strindex.split('_')
    operator, qubits = _parser_header(header)
    stdindex = operator, tuple(qubits), tuple(params)
    return stdindex


def tupindex2stdindex(tupindex):
    '''tupindex to stdindex
    与 strindex 相比，将参数独立，避免参数的格式转换
    Parameters:
        index: str or tuple(str,*params), 
            参考 strindex2stdindex，将参数从字符串分离，
            例如，'X', ('U',0,180), 'iSwap(Q1,Q2)', ('CRz(Q1,Q2)',90)
    Return: stdindex,
        (operator, tuple(qubit), tuple(params))
    '''
    if isinstance(tupindex, str):
        header, params = tupindex, tuple()
    else:
        header, params = tupindex
    operator, qubits = _parser_header(header)
    stdindex = operator, tuple(qubits), tuple(params)
    return stdindex


def stdindex2tupindex(stdindex):
    operator, qubits, params = stdindex
    if len(qubits) > 1:
        header = f"{operator}({','.join(qubits)})"
    else:
        header = operator

    if len(params) > 0:
        tupindex = (header, *params)
    else:
        tupindex = header
    return tupindex


def stdindex2strindex(stdindex):
    operator, qubits, params = stdindex
    if len(qubits) > 1:
        header = f"{operator}({','.join(qubits)})"
    else:
        header = operator

    strindex = '_'.join((header, *(str(p) for p in params)))
    return strindex


def index_convert(index, fr='tupindex', to='stdindex'):
    '''index转换的统一接口'''
    if fr != to:
        cov_dict = {
            ('tupindex', 'stdindex'): ('tupindex', 'stdindex'),
            ('stdindex', 'tupindex'): ('stdindex', 'tupindex'),

            ('strindex', 'stdindex'): ('strindex', 'stdindex'),
            ('stdindex', 'strindex'): ('stdindex', 'strindex'),

            ('strindex', 'tupindex'): ('strindex', 'stdindex', 'tupindex'),
            ('tupindex', 'strindex'): ('tupindex', 'stdindex', 'strindex'),
        }
        cov = cov_dict[(fr, to)]
        cov_funcs = (eval(f'{cov[i]}2{cov[i+1]}') for i in range(len(cov)-1))

        for cov_func in cov_funcs:
            index = cov_func(index)
    return index

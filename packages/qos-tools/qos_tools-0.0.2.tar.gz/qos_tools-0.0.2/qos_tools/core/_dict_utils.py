# Author: lizhiyuan  <lizhiyuan@baqis.ac.cn>  2021/01/01

__all__ = [
    'flatten_dict', 'restore_dict',
]


def flatten_dict(d, symbol='.', level=100):
    '''将多层字典压平为一层
    Parameters:
        d: 待压平的字典
        symbol: 压平所用的连接符号
        level: 压平字典的级数，0为不做操作，默认100级
    Return:
        压平后的字典
    '''
    fd = {}
    for k, v in d.items():
        if isinstance(v, dict) and bool(v) and level > 0:  # v 非空字典
            fd1 = flatten_dict(v, symbol, level-1)
            fd2 = dict(zip((k+symbol+_k for _k in fd1.keys()), fd1.values()))
            fd.update(fd2)
        else:
            fd.update({k: v})
    return fd


def restore_dict(d, symbol='.'):
    '''上面 flatten_dict 函数的逆过程，将压平的字典还原'''
    rd = {}
    for k, v in d.items():
        ks = k.split(symbol)
        _d = rd
        for _k in ks[:-1]:
            _d.setdefault(_k, {})
            _d = _d.get(_k)
        _d.update({ks[-1]: v})
    return rd


def check_dict_template(d, template):
    '''检查字典d是否包含模板字典template中所有的关键字'''
    return flatten_dict(d).keys() >= flatten_dict(template).keys()

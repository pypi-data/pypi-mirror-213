# Author: lizhiyuan  <lizhiyuan@baqis.ac.cn>  2021/01/29

import functools
from qos_tools.fit import function, fitfunc as Function
from qos_tools.fit.fitclass import FitClass


def FitIndex(index='Linear'):
    if isinstance(index, str) and hasattr(Function, index):
        return getattr(Function, index)
    elif isinstance(index, str) and hasattr(function, index):
        fitfunc = getattr(function, index)
        return functools.partial(FitClass, fitfunc=fitfunc)
    elif callable(index):
        return functools.partial(FitClass, fitfunc=index)
    else:
        raise Exception(f'{index} not in FitIndex !')

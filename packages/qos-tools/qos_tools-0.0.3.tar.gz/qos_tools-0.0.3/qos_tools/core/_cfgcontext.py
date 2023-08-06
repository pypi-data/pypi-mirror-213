# Author: lizhiyuan  <lizhiyuan@baqis.ac.cn>  2021/01/01

from contextlib import contextmanager
import numpy as np
import json
import functools

from ._cm import ConsManager


def json_default(obj):
    if isinstance(obj, complex):
        return {'real': obj.real, 'imag': obj.imag}
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    return obj


def json_hook(dic):
    if 'imag' in dic.keys():
        return complex(dic['real'], dic['imag'])
    return dic


def get_dumps_func(backend='json', **kw):
    if backend in ['json']:
        default = dict(sort_keys=False, indent=2, default=json_default)
        default.update(**kw)
        return functools.partial(json.dumps, **default)
    else:
        raise Exception(f'{backend} is not support!')


def get_loads_func(backend='json', **kw):
    if backend in ['json']:
        return functools.partial(json.loads, object_hook=json_hook)
    else:
        raise Exception(f'{backend} is not support!')


def cfgload(fname='config', contrains=None, mode='json', **kw):
    file = f'{fname}.{mode}'
    loads_func = get_loads_func(mode, **kw)

    with open(file, 'r', encoding='utf8') as f:
        s = f.read()
    config = loads_func(s)

    if contrains is not None:
        if callable(contrains):
            _constrains = contrains(config)
        else:
            _constrains = contrains
        cfg = ConsManager(config, _constrains)
        config = cfg.todict()
    return config


def cfgsave(config, fname='config', contrains=None, mode='json', **kw):
    file = f'{fname}.{mode}'
    dumps_func = get_dumps_func(mode, **kw)

    if contrains is not None:
        if callable(contrains):
            _constrains = contrains(config)
        else:
            _constrains = contrains
        cfg = ConsManager(config, _constrains)
        config = cfg.todict()

    s = dumps_func(config)
    with open(file, 'w', encoding='utf8') as f:
        f.write(s)


@contextmanager
def cfgContext(fname='config', contrains=None, mode='json', **kw):
    config = cfgload(fname, contrains, mode, **kw)
    yield config
    cfgsave(config, fname, contrains, mode, **kw)

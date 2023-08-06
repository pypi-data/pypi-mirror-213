# Author: lizhiyuan  <lizhiyuan@baqis.ac.cn>  2021/01/01

import numpy as np

__all__ = [
    'is_equal', 'assert_equal',
]


def is_equal(v1, v2):
    '''深入地比较v1,v2是否相等'''
    try:
        assert_equal(v1, v2)
        return True
    except AssertionError:
        return False


def assert_equal(v1, v2):
    '''断言v1,v2相等'''
    try:
        if isinstance(v1, np.ndarray) or isinstance(v1, np.ndarray):
            assert np.all(v1 == v2)
        else:
            assert v1 == v2
    except ValueError:  # ValueError: The truth value of an array with more than one element is ambiguous. Use a.any() or a.all()
        if isinstance(v1, dict) and isinstance(v2, dict):
            assert not set(v1.keys()) ^ set(v2.keys()), 'keys not equal !'
            for k in v1.keys():
                _v1, _v2 = v1[k], v2[k]
                assert_equal(_v1, _v2)
        elif isinstance(v1, (list, tuple, set)) and isinstance(v2, (list, tuple, set)):
            for _v1, _v2 in zip(v1, v2):
                assert_equal(_v1, _v2)
        else:
            assert False

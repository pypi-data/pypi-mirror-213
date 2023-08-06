# Author: lizhiyuan  <lizhiyuan@baqis.ac.cn>  2021/01/01

from ._equal_utils import is_equal
from ._dict_utils import flatten_dict
from blinker import Signal
import asyncio
import logging
log = logging.getLogger(__name__)


class ConsManager(object):
    '''
    约束管理器

    按照给定的约束规则，管理一个容器内部的约束关联
    '''

    def __init__(self, container, constrains=[], init=True, delimiter='.'):
        '''
        Parameters:
            container: object
                一个类字典的容器，支持方括号索引的形式设置和读取，或支持set/get方法

            constrains: list
                约束条目，每个元素都为一个三元元组（deps, func, target），例如，
                [
                    (('k1.k11','k1.k12'),   (lambda v1,v2:v1+v2),   'k2'       ),
                    (('k3','k4'),           (lambda v1,v2:(v1,v2)), ('k5','k6')),
                ]

            init: bool, optional
                是否使用约束条件初始化传入的字典，默认 True

            delimiter: str, optional
                分割符，默认 .
        '''
        self.container = container
        self.delimiter = delimiter
        self.sig = Signal()
        # 如果约束的 func 是字符串，则 eval
        _constrains = []
        for deps, func, target in constrains:
            if isinstance(func, str):
                func = eval(func)
            _constrains.append((deps, func, target))

        self.constrains = _constrains
        self.key_changed = set()  # 集合，记录改变的key，留出接口
        self.subscribers = self.__init_cons(_constrains, init=init)

    def __init_cons(self, constrains, init=True):
        subscribers = []
        for deps, func, target in constrains:
            subs = _subscrib(deps, func, target, self)
            subscribers.append(subs)
            for _k in deps:
                self.sig.connect(subs, sender=_k)
        if init:
            deps_set = set()
            for deps, func, target in constrains:
                deps_set.update(deps)
            for dep in deps_set:
                self._send(dep)
        return subscribers

    def _send(self, key):
        self.sig.send(key)
        self.key_changed.add(key)
        _k_list = key.rsplit(self.delimiter, maxsplit=1)
        if len(_k_list) > 1:
            self._send(_k_list[0])

    def _set(self, key, value, check=True):
        '''根据关键词连接的字符串，设置对应的值

        Parameters:
            key: str or list
                使用符号串联关键词的字符串，比如'pulse.width.value'

            value: 
                待设入的值

            check: bool
                是否检查设入值与原值相等
        Return: 
            bool, True 表示value改变并且已设置，False 表示未变
        '''
        ks = key.rsplit(self.delimiter,maxsplit=1)
        if len(ks) > 1:
            _ks, _k = ks[0], ks[1]
            _ct = self.get(_ks)
        else:
            _k = key
            _ct = self.container
        assert _ct is not None, f"key '{key}' not exist !"

        if check and is_equal(value, _ct.get(_k)):
            return False
        else:
            try:
                _ct[_k] = value
            except TypeError:  # object is not subscriptable
                _ct.set(_k, value)
            except Exception as e:
                raise e
            return True
    
    def set(self, key, value, check=True):
        is_changed = self._set(key, value, check=check)
        if is_changed:
            self._send(key)

    def get(self, key, default=None):
        '''根据关键词连接的字符串或者列表，获取对应的值

        Parameters:
            key: str or list
                使用符号串联关键词的字符串，比如'pulse.width.value'

            default: 
                类似于字典方法，当关键词不存在时返回一个默认值

        Return:
            返回键值串对应的值
        '''
        ks = key.split(self.delimiter)
        _v = self.container
        for k in ks:
            try:
                _v = _v[k]
            except KeyError:
                _v = default
            except TypeError:  # object is not subscriptable
                _v = _v.get(k)
            except Exception as e:
                raise e
        return _v

    def update(self, d, check=True):
        '''批量更新信息

        Parameters:
            d: dict
                待更新信息的字典

            check: bool,optional
                是否检查设入值与原值相等
        '''
        k_changed = []
        d_flatten = flatten_dict(d, self.delimiter)
        for k, v in d_flatten.items():
            _changed = self._set(k, v, check=check)
            if _changed:
                k_changed.append(k)
        for _k in k_changed:
            self._send(_k)


def _subscrib(deps, func, target, cons_manager):
    '''订阅函数生成器

    根据需要的参量产生一个订阅函数

    Parameters:
        deps,func,target: 
            依赖关键词[列表或元组]，约束函数，目标关键词[单key(字符串)，或者多key(列表/元组)]，
            比如 (('k1','k2'), lambda v1,v2:v1+v2, 'k3'), func的返回值应与target数目一致

        cons_manager: object
            ConsManager的一个实例

    Return:
        返回一个订阅函数
    '''
    def subscriber(send):
        arg = [cons_manager.get(k_dep) for k_dep in deps]
        if None not in arg:
            if asyncio.iscoroutinefunction(func):
                loop = asyncio.get_event_loop()
                task = func(*arg)
                value = loop.run_until_complete(task)
            else:
                value = func(*arg)
            if isinstance(target, str):
                cons_manager.set(target, value)
            else:
                d = dict(zip(target, value))
                cons_manager.update(d)
        else:  # 这里只打出警告：一些依赖变量的值为None，打印出所有的键值对
            log.warning(f'{__name__} WARNING: ' +
                        ', '.join([f'{k} is {v}' for k, v in zip(deps, arg)]))
    return subscriber

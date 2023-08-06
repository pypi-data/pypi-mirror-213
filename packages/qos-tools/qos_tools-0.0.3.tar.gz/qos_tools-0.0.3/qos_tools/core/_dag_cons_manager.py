# Author: lizhiyuan  <lizhiyuan@baqis.ac.cn>  2021/01/01
# rebuild  2021/08/19

import queue
import threading
from qos_tools.core._equal_utils import is_equal
from qos_tools.core._dict_utils import flatten_dict
from qos_tools.core._graph_func import get_subgraph, extract_graph
from graphlib import TopologicalSorter
import asyncio
import logging
log = logging.getLogger(__name__)


def default_worker(task_queue, result_queue, executor=None):
    '''
    task_queue/result_queue: queue.Queue的实例化对象
    executor: 执行器
    '''
    while True:
        if task_queue.qsize():
            task_func, args, kwds = task_queue.get()
            if executor is None:
                result = task_func(*args, **kwds)
            else:
                # TODO：根据执行器接口定义
                raise
            task_queue.task_done()
            result_queue.put(result)


def creat_task(deps, func, targets, cons_manager):
    def task_func(*args, **kwds):
        if None not in args:
            if asyncio.iscoroutinefunction(func):
                tsk = func(*args)
                value = asyncio.run(tsk)
            else:
                value = func(*args)
            return dict(zip(targets, value))
        else:  # 这里只打出警告：一些依赖变量的值为None，打印出所有的键值对
            log.warning(f'{__name__} WARNING: ' +
                        ', '.join([f'{k} is {v}' for k, v in zip(deps, args)]))
            try:
                if asyncio.iscoroutinefunction(func):
                    tsk = func(*args)
                    value = asyncio.run(tsk)
                else:
                    value = func(*args)
                return dict(zip(targets, value))
            except Exception as e:
                log.warning(f'{__name__} WARNING: '+str(e))
                return {}

    args = tuple(cons_manager.get(dep) for dep in deps)
    kwds = dict()

    task_flag = (deps, targets)
    task = (task_func, args, kwds)
    return task_flag, task


class DagConsManager(object):
    '''
    约束管理器

    按照给定的约束规则，管理一个容器内部的约束关联
    '''

    def __init__(self, container, constrains=[], delimiter='.', executor=None):
        '''
        Parameters:
            container: object
                一个类字典的树状容器，每一级都支持方括号索引的形式设置读取，或支持set/get方法设置读取

            constrains: list
                约束条目，每个元素都为一个三元元组（deps, func, targets），例如，
                [
                    (('k1.k11','k1.k12'),   (lambda v1,v2:v1+v2),   'k2'       ),
                    (('k3','k4'),           (lambda v1,v2:(v1,v2)), ('k5','k6')),
                ]
                deps，元组
                func，函数或可eval的函数表达式字符串
                targets，字符串或元组，于func输出格式一致

            delimiter: str, optional
                分割符，默认 .

            executor: 执行器
                接口参考default_worker
        '''
        self.container = container
        self.delimiter = delimiter

        constrains_dict = {}
        tar_dict = {}
        tar_list = []
        for deps, func, targets in constrains:
            if isinstance(func, str):  # 如果约束的 func 是字符串，则 eval
                func = eval(func)
            if isinstance(targets, str):
                targets = (targets,)
                func_ = lambda *args, **kw: (func(*args, **kw),)
            else:
                func_ = func
            constrains_dict[(deps, targets)] = (deps, func_, targets)
            for tar in targets:
                tar_dict[tar] = (deps, targets)
                assert tar not in tar_list, f"The target '{tar}' appears repeatedly in multiple constrain items"
                tar_list.append(tar)

        self.constrains_dict = constrains_dict
        self.tar_dict = tar_dict
        self.graph_forward, self.graph_backward = extract_graph(constrains)
        ts = TopologicalSorter(self.graph_forward)
        self.static_order = list(ts.static_order())

        # turn-on the worker thread
        self.task_queue = queue.Queue()
        self.result_queue = queue.Queue()
        self.Thread = threading.Thread(target=default_worker, args=(
            self.task_queue, self.result_queue, executor), daemon=True)
        self.Thread.start()

    def _set(self, key, value, check=True):
        '''根据关键词连接的字符串，设置对应的值

        Parameters:
            key: str
                使用符号串联关键词的字符串，比如'pulse.width.value'

            value: 
                待设入的值

            check: bool
                是否检查设入值与原值相等
        Return: 
            bool, True 表示value改变并且已设置，False 表示未变
        '''
        ks = key.rsplit(self.delimiter, maxsplit=1)
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
            self.exec_dag([key])
        return is_changed

    def get(self, key, default=None):
        '''根据关键词连接的字符串，获取对应的值

        Parameters:
            key: str
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
        keys_changed = []
        d_flatten = flatten_dict(d, self.delimiter)
        for k, v in d_flatten.items():
            is_changed = self._set(k, v, check=check)
            if is_changed:
                keys_changed.append(k)
        self.exec_dag(keys_changed)

    def exec_dag(self, keys_changed):
        '''根据传入的节点列表，通过有向图的方式执行约束函数
        keys_changed: 发生了变化的节点的列表
        '''
        subgraph_nodes = set(keys_changed) & set(self.static_order)
        subgraph = get_subgraph(
            subgraph_nodes, graph_backward=self.graph_backward)
        ts = TopologicalSorter(subgraph)
        ts.prepare()
        count = 0
        while ts.is_active():
            task_dict = {}
            for node in ts.get_ready():
                if count == 0:
                    ts.done(node)
                else:
                    deps, func, targets = self.constrains_dict[self.tar_dict[node]]
                    task_flag, task = creat_task(deps, func, targets, self)
                    task_dict[task_flag] = task
            for task in task_dict.values():
                self.task_queue.put(task)

            if self.result_queue.qsize():
                result = self.result_queue.get()
                self.result_queue.task_done()
                for k, v in result.items():
                    self._set(k, v, check=False)
                    ts.done(k)
            count += 1

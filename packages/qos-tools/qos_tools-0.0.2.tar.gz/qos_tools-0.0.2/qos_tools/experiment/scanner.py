# Author: Liu Pei  <liupei200546@163.com>  2021/08/14

from graphlib import TopologicalSorter
from typing import Any, Callable, Optional

from kernel.sched import App
from qos_tools.gatemap import circuit_convert


def topological_order_of_constrains(constrains_list: list[tuple]) -> tuple[dict, dict, dict]:
    """
    Return the topological order of constrains list and other messages for calculation.

    Args:
        constrains_list (list): list[(keys, func, goal)]

    Raises:
        ValueError: [description]

    Returns:
        tuple[dict, dict, dict]: {goal:constrains}, {key(hashable object): list}, {key(hashable object): order(int)}
    """

    graph_core = TopologicalSorter()

    node_set = set()
    goal_set = set()
    constrains_dict = {}

    for keys, func, goal in constrains_list:
        if goal in goal_set:
            raise ValueError('This constrains is illegal.')
        else:
            goal_set.add(goal)
            node_set.add(goal)
            for ks in keys:
                node_set.add(ks)
            graph_core.add(goal, *keys)
            constrains_dict[goal] = (keys, func, goal)

    constrains_next = {item: [] for item in node_set}
    for keys, func, goal in constrains_list:
        for k in keys:
            constrains_next[k].append(goal)

    try:
        order = graph_core.static_order()
        order_dict = {item: i for i, item in enumerate(order)}
        return constrains_dict, constrains_next, order_dict
    except Exception as e:
        print(e)
        return {}, {}, {}


class Scanner(App):
    """
    Basic class for Scanner class. Change a config of scanning into a App(Task) object. Support the constrans updating.
    """

    def __init__(self, name: str, qubits: list[int], scanner_name: str = '', **kw):
        """
        Init.

        Args:
            name (str): the name of this experiment.
            qubits (list[int]): the qubits which are acted on.
            scanner_name (str): Defaults to None.
        """

        self._name = name
        self.qubits = qubits

        super().__init__(**kw)

        self.meta_info['scanner'] = scanner_name

    def init(self, sweep_config: dict, sweep_setting: dict, setting: dict, constrains: list = [],
             sweep_addition: dict = {}, mask_func: Optional[Callable] = None,
             plot_setting: Optional[dict] = None, plot: list[list[str]] = [['', ''], ['', '']], **kw):
        """
        Init.

        Args:
            sweep_config (dict): main for sweep addr.
            sweep_setting (dict): sweep list for scan_iters.
            setting (dict): setting for this scanner.
            constrains (list, optional): constrains for this scanner. Defaults to [].
            sweep_addition (dict, optional): addition message for scan_iters. Defaults to {}.
            mask_func (Optional[Callable], optional): filter in scan_iters. Defaults to None.
            plot_setting (Optional[dict], optional): use in UI. Defaults to None.
            plot (list[list[str]], optional): use in UI. Defaults to [['', ''], ['', '']].
        """

        self.sweep_config = sweep_config
        self.sweep_setting = sweep_setting
        self.sweep_addition = sweep_addition

        self.setting = setting
        self.setting['skip'] = 0
        self.constrains, self.constrains_next, self.constrains_order = topological_order_of_constrains(
            constrains)

        if isinstance(mask_func, str):
            mask_func = eval(mask_func)
        self.mask_func = mask_func

        self.plot_setting = plot_setting

        self.meta_info['name'] = self.name
        self.meta_info['axis'] = self.plot_setting

        self.meta_info['plot'] = plot

    def get(self, key: str, task=None) -> Any:
        """
        get from self.setting and cached config. 

        Args:
            key (str): str, `.setting` allowed query as attribute.
            task ([type], optional): ScannerNode use. Defaults to None.

        Raises:
            e: failed in fetching keys

        Returns:
            Any: value
        """
        ks = key.split('.') if isinstance(key, str) else key
        if ks[0] in ['setting']:
            _v = self.setting
            for k in ks[1:]:
                try:
                    _v = _v[k]
                except TypeError:
                    _v = _v.get(k)
                except Exception as e:
                    raise e
            # print(f'get key = {key}, value = {_v}')
            return _v
        else:
            # print(f'get key = {key}, value = {super().get(key)}')
            if task is not None:
                return task.get(key)
            else:
                return super().get(key)

    def set(self, key: str, value: Any, task=None) -> None:
        """
        set in self.setting and cached config. 

        Args:
            key (str): `.setting` allowed query as attribute.
            value (Any): value. 
            task ([type], optional): ScannerNode use. Defaults to None.

        Raises:
            e: failed in fetching keys
        """

        if key is None:
            return

        ks = key.split('.') if isinstance(key, str) else key
        if ks[0] in ['setting']:
            if len(ks) > 1:
                _ks, _k = ks[:-1], ks[-1]
                _ct = self.get(_ks)
            else:
                _k = key
                _ct = self.setting
            assert _ct is not None, f"key '{key}' not exist !"

            if value == _ct.get(_k):
                pass
            else:
                try:
                    _ct[_k] = value
                except TypeError:  # object is not subscriptable
                    _ct.set(_k, value)
                except Exception as e:
                    raise e
        else:
            # print(f'set key = {key}, value = {value}')
            if task is not None:
                task.set(key, value, False)
            else:
                super().set(key, value, False)

    def update(self, update_dict: dict, task=None) -> int:
        """
        Update parameters under constraint check.

        Args:
            update_dict (dict): {key:value} to be updated.
            task ([type], optional): ScannerNode use. Defaults to None.

        Raises:
            ValueError: There are contradictions in the update, please check the constraint relationship.

        Returns:
            int: the flag whether self.skip is updated in this updating.
        """

        last_skip = self.setting['skip']+0

        to_update_flag_dict = {
            item: False for item in self.constrains_order.keys()}

        for keys in self.constrains_order.keys():

            if keys in update_dict.keys():
                value = update_dict[keys]
                if to_update_flag_dict[keys]:
                    ks = [self.get(k, task=task)
                          for k in self.constrains[keys][0]]
                    if value != self.constrains[keys][1](*ks):
                        raise ValueError(
                            'There are contradictions in the update, please check the constraint relationship.')
                    else:
                        self.set(keys, value, task=task)
                else:
                    if keys in self.constrains.keys():
                        print(
                            'Warning! The relationship before the constraint is not checked')
                    self.set(keys, value, task=task)
                    for ks in self.constrains_next[keys]:
                        to_update_flag_dict[ks] = True
            elif to_update_flag_dict[keys]:
                ks = [self.get(k, task=task) for k in self.constrains[keys][0]]
                self.set(keys, self.constrains[keys][1](*ks), task=task)
                for ks in self.constrains_next[keys]:
                    to_update_flag_dict[ks] = True

        for keys, value in update_dict.items():
            if keys not in self.constrains_next.keys():
                self.set(keys, value, task=task)

        return self.setting['skip'] > 0 and last_skip != self.setting['skip']

    @property
    def name(self) -> str:
        return self._name

    def scan_range(self) -> dict:
        return {
            'iters': self.sweep_setting,
            'filter': self.mask_func,
            'additional_kwds': self.sweep_addition,
        }

    def main(self, task=None) -> None:
        """
        Main process in a linear scanner.

        Args:
            task ([type], optional): ScannerNode use. Defaults to None.
        """
        self.update(self.setting['pre_setting'], task=task)

        for step in self.scan() if task is None else task.scan():

            skip = self.update(
                {self.sweep_config[k]['addr']: v for k, v in step.kwds.items()}, task=task)
            circuit = circuit_convert(
                self.setting['circuit'], fr=self.setting['circuit_type'], to='cmds:qlispcmd')
            if task is None:
                self.exec(
                    circuit, skip_compile=skip and not self.setting['compile_once'])
            else:
                task.exec(
                    circuit, skip_compile=skip and not self.setting['compile_once'])

# Author: Liu Pei  <liupei200546@163.com>  2021/08/14

from graphlib import TopologicalSorter
from typing import Any, Callable, Optional

from kernel.sched import App
from qos_tools.gatemap import circuit_convert
from waveforms.scan_iter import Begin, End


def topological_order_of_constrains(
        constrains_list: list[tuple]) -> tuple[dict, dict, dict]:
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

    # NOTE : 
    # here seems like to use the library sorter to sort the constrans_list
    # where ks must be a collection of stuff same type(hashable) as goal, that
    # are the predesessor of this node, the node signature is goal,
    # the constrains_list is composed in the form like 
    #[
    #   (ks, f , goal)
    #   (ks, f , goal)
    #   ... 
    #   (ks, f , goal)
    #]
    # the first thing to returns is just A[goal] = (ks,f,goal)
    # the second return is the reversed edge direciton of A
    # the third is the order 
    # 
    # questions : 
    # 1. is this a closed graph. aka k in ks are in all the goals ? 
    # 2. topo sort did not make sure the key to be scanned to appear
    #   as close to the rear as possible 
    #   so that the repeatative tasks are done less.
    for keys, func, goal in constrains_list:
        if goal in goal_set:
            # the goal never repeat
            raise ValueError('This constrains is illegal.')
        else:
            goal_set.add(goal)
            node_set.add(goal)
            for ks in keys:
                node_set.add(ks) ; 
            # both the ks and goal is added into the node_set 
            graph_core.add(goal, *keys);# builidng the constraint_list into sorted graph
            constrains_dict[goal] = (keys, func, goal)

    # cn is the closed graph in this descripion.
    constrains_next = {item: [] for item in node_set}
    #{
    #  closed_goal :[]
    #}

    # reversing direction
    for keys, func, goal in constrains_list:
        for k in keys:
            constrains_next[k].append(goal)
    #{
    #   "w" :[ "n" that  "w"  depends on ] # contraints_dict like
    #   
    #   "w" :[ "n" that  depend on "w"] # constraints_next like
    #}
    try:
        order = graph_core.static_order()
        order_dict = {item: i for i, item in enumerate(order)} ;
        return constrains_dict, constrains_next, order_dict
    except Exception as e:
        # only exception should be the loop
        print(e)
        # why return if there is error ? 
        return {}, {}, {}


class Scanner(App):
    """
    Basic class for Scanner class. Change a config of scanning into a App(Task) object. Support the constrans updating.
    """
    #NOTE : This code is so bloated.
    def __init__(self,
                 name: str,
                 qubits: list[int],
                 scanner_name: str = '',
                 **kw):
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

    def init(self,
             sweep_config: dict = {},  # the configuration battery
             sweep_setting: dict = {}, # here defines what is to be scanned
             setting: dict = {},      # feed,feedback skip...
             constrains: list = [],   # the things to be used in topo sort
             sweep_addition: dict = {}, # why not just add this to the battery ? 
             sweep_trackers: list = [], # to take note on additional data
             sweep_filter: Optional[Callable] = None, 
             **kw): # this kws are for this Scanner, but not fore the App
        """
        Init.

        Args:
            sweep_config (dict, optional): main for sweep addr. Defaults to {}.
            sweep_setting (dict, optional): sweep list for scan_iters. Defaults to {}.
            setting (dict, optional): setting for this scanner. Defaults to {}.
            constrains (list, optional): constrains for this scanner. Defaults to [].
            sweep_addition (dict, optional): addition message for scan_iters. Defaults to {}.
            sweep_trackers (list, optional): list of tracker objclass. Defaults to [].
            sweep_filter (Optional[Callable], optional): filter in scan_iters. Defaults to None.
        """

        # recording without copy
        self.sweep_config = sweep_config
        self.sweep_setting = sweep_setting
        self.sweep_addition = sweep_addition
        self.sweep_trackers = sweep_trackers
        self.sweep_filter = sweep_filter

        self.setting = setting
        # adding a key
        self.setting['skip'] = 0
        
        # sort
        self.constrains, self.constrains_next, self.constrains_order = topological_order_of_constrains(
            constrains)

        
        if 'feedback' in setting.keys():
            self._cache = []
            assert setting.get(
                'level_marker', False), '`level_marker` must be True.'
            assert isinstance(setting['feedback'],
                              dict), '`feedback` must be a dict.'
            
            #XXX usually it is  (key,value) for dict.items.
            for value, key in setting['feedback'].items():
                assert isinstance(value, int) and isinstance(
                    key, Callable), 'Form of `feedback` is invalid.'
        # setting['feedback'] is like 
        # { 
        #   5 : f , 
        # } 

        if 'feed' in setting.keys():
            assert isinstance(
                setting['feed'], Callable), 'Method for feed of tracker does not exist.'
        # setting['feed'] is like : [ f ] 

    # hieracial dictionary with . as seperation
    # NOTE : did not iterate through list though.
    def get(self, key: str) -> Any:
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
                # rec sink point
                # NOTE : cant the bottom types all just overide __getitem__ and __setitem__?
                try:
                    _v = _v[k]
                except TypeError:
                    _v = _v.get(k) 
                except Exception as e:
                    raise e
            return _v
        else:
            return super().get(key)

    def set(self, key: str, value: Any):
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
                _ct = self.get(_ks); # recursive sink point
            else:
                _k = key
                _ct = self.setting;
            #NOTE : should create the key path if not exist.
            assert _ct is not None, f"key '{key}' not exist !" 

            if value == _ct.get(_k):
                pass
            else:
                try:
                    _ct[_k] = value
                except TypeError:
                    # why is this a type error?
                    _ct.set(_k, value)
                except Exception as e:
                    # this action is not nessesary
                    raise e
        else:
            # letting the app do it.
            super().set(key, value, False)

    def update(self, update_dict: dict):
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

        to_update_flag_dict = {
            item: False
            for item in self.constrains_order.keys()
        } # the check table 

      
        for keys in self.constrains_order.keys(): 
            # the "key" not the "keys" is integer order index
            if keys in update_dict: 
                value = update_dict[keys]
                if to_update_flag_dict[keys]:
                    ks = [
                        self.get(k)
                        for k in self.constrains[keys][0]
                    ]
                    if value != self.constrains[keys][1](*ks):
                        raise ValueError(
                            'There are contradictions in the update, please check the constraint relationship.'
                        )
                    else:
                        self.set(keys, value)
                else:
                    if keys in self.constrains.keys():
                        print(
                            'Warning! The relationship before the constraint is not checked'
                        )
                    self.set(keys, value)
                    for ks in self.constrains_next[keys]:
                        to_update_flag_dict[ks] = True
            elif to_update_flag_dict[keys]:
                ks = [self.get(k) for k in self.constrains[keys][0]]
                self.set(keys, self.constrains[keys][1](*ks))
                for ks in self.constrains_next[keys]:
                    to_update_flag_dict[ks] = True

        for keys, value in update_dict.items():
            if keys not in self.constrains_next.keys():
                self.set(keys, value)

    @property
    def name(self) -> str:
        return self._name

    def scan_range(self) -> dict:
        return {
            'loops': self.sweep_setting,
            'filter': self.sweep_filter,
            'functions': self.sweep_addition,
            'trackers': self.sweep_trackers,
            'level_marker': self.setting.get('level_marker', False)
        }

    def main(self):
        """
        Main process in a linear scanner.

        Args:
            task ([type], optional): ScannerNode use. Defaults to None.
        """
        self.update(self.setting.get('pre_setting', {}))

        last_skip = 0

        circuit = self.setting.get('circuit', [])
        convert_flag = self.setting.get('circuit_type', 'cmds:qlispcmd') != 'cmds:qlispcmd'
        feed_func = self.setting.get('feed', None)

        _cache_flag = self.setting.get('level_marker', False)

        for step in self.scan():

            if isinstance(step, Begin):
                continue
            elif isinstance(step, End):
                if step.level in self.setting['feedback'].keys():
                    self.flush()
                    self.setting['feedback'][step.level](self, step)

            else:
                skip = step.kwds.get('skip', last_skip)
                circuit = step.kwds.get('circuit', circuit)
                if convert_flag:
                    circuit = circuit_convert(
                        circuit, fr=self.setting['circuit_type'], to='cmds:qlispcmd')
                self.update(
                    {
                        v_dict['addr']: step.kwds[k]
                        for k, v_dict in self.sweep_config.items()
                    })
                tmp = self.exec(circuit, skip_compile=((
                    skip > 0) and (last_skip != skip) and (not self.setting.get('compile_once', False))))
                if _cache_flag:
                    self._cache.append(tmp)
                last_skip = skip

                if feed_func is not None:
                    feed_func(self, step)

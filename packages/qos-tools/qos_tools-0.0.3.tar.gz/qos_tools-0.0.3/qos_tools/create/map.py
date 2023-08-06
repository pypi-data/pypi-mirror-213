# Author: Liu Pei  <liupei200546@163.com>  2022/03/15

from typing import Optional

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from networkx import Graph


class Mapping(Graph):

    _update_flag = False
    _qubit_neighbors = {}
    _direct_coupler_count = 0

    cmap = 'nipy_spectral'
    allowed_type = ['Q', 'C', 'D', 'M', 'J']
    type_color = {'Q': 0, 'C': 1, 'D': 2, 'M': 3, 'J': 4}
    place_holder = '*'

    def check_type(self):
        for item in self.nodes:
            assert self.nodes[item]['type'] in self.allowed_type, 'Invalid type of components.'

    def _dfs(self, node, deep: Optional[int] = None, condition: Optional[list[str]] = None):

        def _check_condition(node, condition):
            return condition == self.place_holder or self.nodes[node]['type'] == condition

        def __dfs(deep, condition, dis, stack, ret, flag):
            if dis+1 >= deep:
                ret.append(tuple(stack))
            else:
                for item in self.neighbors(stack[dis]):
                    if _check_condition(node=item, condition=condition[dis+1]) and flag[item]:
                        stack[dis+1], flag[item] = item, False
                        __dfs(deep=deep, condition=condition, dis=dis +
                              1, stack=stack, ret=ret, flag=flag)
                        flag[item] = True

        if condition is None and deep is None:
            raise KeyError('Free parameters for dfs are not supported')

        self.check_type()

        if condition is None:
            condition = [self.place_holder]*deep
        elif deep is None:
            deep = len(condition)

        ret = []

        if not _check_condition(node=node, condition=condition[0]):
            return ret

        stack, flag = [node]*deep, {item: True for item in self.nodes}
        flag[node] = False

        __dfs(deep=deep, condition=condition, dis=0,
              stack=stack, ret=ret, flag=flag)
        return ret

    def _add_components(self, components: list[str], type: str):
        assert type in self.allowed_type, 'Invalid type of components.'
        self.add_nodes_from(components, type=type)
        self._update_flag = True

    def add_qubits(self, qubits: list[str], type: str = 'Q'):
        self._add_components(qubits, type)

    def add_coupler(self, coupler: str, qubits: list[str], type: str = 'C'):
        self._add_components([coupler], type)
        self.add_edges_from([(coupler, q) for q in qubits])

    def add_direct_couple(self, qubits: list[str], type: str = 'D'):
        self._direct_coupler_count += 1
        self._add_components([f'D{self._direct_coupler_count}'], type)
        self.add_edges_from(
            [(f'D{self._direct_coupler_count}', q) for q in qubits])
        return f'D{self._direct_coupler_count}'

    def add_probe(self, probe, qubits: list[str], type: str = 'M'):
        self._add_components([probe], type)
        self.add_edges_from([(probe, q) for q in qubits])

    def add_jpa(self, jpa, probes: list[str], type: str = 'J'):
        self._add_components([jpa], type)
        self.add_edges_from([(jpa, p) for p in probes])

    def _draw_node_config(self, tag, ndim):
        ret = {'cmap': self.cmap}
        vmin, vmax = 1e50, -1e50
        if tag is None:
            ret['node_color'] = [self.type_color[self.nodes[item]['type']]
                                 for item in self.nodes]
        else:
            ret['nodelist'] = []
            ret['node_color'] = []
            ret['labels'] = {}
            for item in self.nodes:
                value = self.nodes[item].get(tag, np.nan)
                if np.isnan(value):
                    continue
                ret['node_color'].append(value)
                label_output = '{x:.%df}' % ndim
                ret['labels'][item] = label_output.format(x=value)
                ret['nodelist'].append(item)
                vmin, vmax = min(vmin, value), max(vmax, value)

        return ret, vmin if vmin<1e50 else 0, vmax if vmax>-1e50 else 1

    def draw(self, tag: Optional[str] = None, layout: str = 'spring_layout', seed=1234, colorbar: bool = True,
             font_size=8, alpha=1, font_color='w', ndim: int = 0, **kw):
        from networkx import layout as layout_lib
        if 'pos' not in kw.keys():
            kw['pos'] = getattr(layout_lib, layout)(self, seed=seed)
        update_config, vmin, vmax = self._draw_node_config(tag=tag, ndim=ndim)
        kw.update(update_config)
        nx.draw_networkx(self, with_labels=True, font_size=font_size,
                         font_color=font_color, alpha=alpha, **kw)
        if 'ax' in kw.keys():
            ax = kw['ax']
            ax.set_yticks([])
            ax.set_xticks([])
            for i in ['bottom', 'top', 'right', 'left']:
                ax.spines[i].set_visible(False)
            if isinstance(tag, str):
                ax.set_title(tag)
            if tag is not None and colorbar:
                self.colorbar(ax=ax, vmin=vmin, vmax=vmax)

    def colorbar(self, fraction: float = 0.1, shrink: float = 0.5, vmin: float = 0, vmax: float = 1, **kw):
        from matplotlib.cm import ScalarMappable
        scaler = ScalarMappable(cmap=self.cmap)
        scaler.set_clim(vmin=vmin, vmax=vmax)
        plt.colorbar(scaler, fraction=fraction, shrink=shrink, **kw)

    def component_neighbors(self, node, deep: Optional[int] = None, condition: Optional[list[str]] = None):
        return self._dfs(node, deep, condition)

    def clear(self):
        self._direct_coupler_count = 0
        super().clear()


def config2mapping(keys: list[str], query: callable) -> Mapping:
    """
    From a query method to create a `Mapping` class. 

    Args:
        keys (list[str]): keys list from config.
        query (callable): query method

    Returns:
        Mapping: Graph object.
    """
    ret = Mapping()
    qubits = [key for key in keys if key[0] == 'Q']
    ret.add_qubits(qubits=qubits)
    for item in keys:
        if item[0] == 'C':
            ret.add_coupler(item, query(f'{item}.qubits'))
        elif item[0] == 'M':
            ret.add_probe(item, query(f'{item}.qubits'))
        elif item[0] == 'J':
            ret.add_jpa(item, query(f'{item}.probe'))
        else:
            pass
    return ret


def mapping2cfg(map: Mapping, update: callable):
    """
    From a `Mapping` method to update a config

    Args:
        map (Mapping): Graph object.
        update (callable): update method of config
    """

    from itertools import combinations

    from .create import (create_coupler, create_probe, create_qubit,
                         gate_mapping_1, gate_mapping_2)

    gates = {gate: {}
             for gate in list(gate_mapping_1.keys())+list(gate_mapping_2.keys())}
    for item in map.nodes:
        if map.nodes[item]['type'] == 'Q':
            couplers, probe = [], None
            for goal in map.neighbors(item):
                if map.nodes[goal]['type'] == 'C':
                    couplers.append(goal)
                elif map.nodes[goal]['type'] == 'M':
                    probe = goal
            update(item, create_qubit(probe=probe, couplers=couplers))

            for gate in gate_mapping_1.keys():
                gates[gate][item] = gate_mapping_1[gate]()

        elif map.nodes[item]['type'] == 'C':
            qubits = []
            for goal in map.neighbors(item):
                if map.nodes[goal]['type'] == 'Q':
                    qubits.append(goal)
            update(item, create_coupler(qubits=qubits))
        elif map.nodes[item]['type'] == 'M':
            qubits = []
            for goal in map.neighbors(item):
                if map.nodes[goal]['type'] == 'Q':
                    qubits.append(goal)
            update(item, create_probe(qubits=qubits))

    for gate in gate_mapping_2.keys():
        for _type, method in gate_mapping_2[gate]:
            for item in map.nodes:
                if map.nodes[item]['type'] == _type:
                    for q1, q2 in combinations([goal for goal in map.neighbors(item) if map.nodes[goal]['type'] == 'Q'], 2):
                        gates[gate][f'{q1}_{q2}'] = method()

    update('gate', gates)

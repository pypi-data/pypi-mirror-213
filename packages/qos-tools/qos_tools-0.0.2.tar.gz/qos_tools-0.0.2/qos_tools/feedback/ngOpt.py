# Author: Liu Pei  <liupei200546@163.com>  2022/07/25

from dataclasses import dataclass
from queue import Queue
from typing import Any, Sequence, Union

import nevergrad as ng
from scipy.optimize import OptimizeResult
from waveforms.scan_iter import BaseOptimizer


@dataclass
class VarData:
    pattern: str = 'mul'
    init: float = 1
    low: float = 0.9
    high: float = 1.1

    def get(self, key, default=None):
        return self.__getattribute__(key)


def init_variable(variable: list[dict]) -> ng.p.Array:
    init, low, high = [], [], []
    for item in variable:
        init.append(item.get('init', 1))
        if item.get('pattern', 'mul') in ['add']:
            low.append(init[-1] + item.get('low', 0.9))
            high.append(init[-1] + item.get('high', 1.1))
        else:
            low.append(init[-1] * item.get('low', 0.9))
            high.append(init[-1] * item.get('high', 1.1))
    return ng.p.Array(init=init, lower=low, upper=high)


class NgOpt(BaseOptimizer):

    def __init__(self,
                 variable: Union[list[dict], list[VarData], ng.p.Array],
                 config: dict = {},
                 **kw):

        self._catch, self._all_x, self._all_y = Queue(), [], []
        self.config = {
            'method': 'TBPSA',
            'budget': 300,
        }

        self.config.update(config)
        if not isinstance(variable, ng.p.Array):
            variable = init_variable(variable=variable)
        self.opt = getattr(ng.optimizers,
                           self.config['method'])(variable,
                                                  budget=self.config['budget'])

    def ask(self):
        tmp = self.opt.ask()
        self._catch.put(tmp)
        return tmp.args[0]

    def tell(self, suggested: Sequence, value: Any):
        if not self._catch.empty():
            tmp = self._catch.get()
            self._all_x.append(tmp.args[0])
            self._all_y.append(value)
            self.opt.tell(tmp, value)

    def get_result(self, history: bool = False) -> OptimizeResult:
        ret = OptimizeResult({'x': self.opt.recommend().args[0]})
        if history:
            ret.x_iters = self._all_x
            ret.func_vals = self._all_y
        return ret

# Author: Liu Pei  <liupei200546@163.com>  2021/10/13

from typing import Any, Literal, Optional

import skopt.space.space as space
from pydantic import BaseModel
from scipy.optimize import OptimizeResult
from skopt import Optimizer

from .model import FeedAgent


class ParaMode(BaseModel):
    pat: Optional[Literal['mul', 'add']] = None
    mode: Optional[Literal['Real', 'Integer']] = None


class BayesOpt(FeedAgent):
    """
    Agend for Bayes optmizer.

    Variable in the form:
    {
        'pattern': (Literal['mul', 'add']): base+bound or base*bound.
        'low' (float): lower bound.
        'high' (float): upper bound.
        'type' (Literal['Real', 'Integer']): parameter type.
    }

    Attribute:
        opt (Optimizer): the `skopt.Optimizer` class
    """

    config = {
        'transform': 'normalize',
        'prior': 'uniform',
        'base_estimator': 'GP',
        'n_initial_points': 10,
        'initial_point_generator': 'hammersly',
    }

    def __init__(self, variable: list[dict], base: list, config: dict = {}, **kw):
        """
        Create a new opt.

        Args:
            variable (list[dict]): variable list.
            base (list): initial value.
            config (dict, optional): optimizer configuration parameters. Defaults to {}.
        """

        self.config.update(config)

        self.variable = []

        for i, item in enumerate(variable):
            self.variable.append(self._add_variable(base=base[i], **item))

        self.opt = Optimizer(self.variable,
                             base_estimator=self.config['base_estimator'],
                             n_initial_points=self.config['n_initial_points'],
                             initial_point_generator=self.config['initial_point_generator'])

    def _add_variable(self, base: Any, pattern: str = 'mul', low: Any = 0.5, high: Any = 1.5, type: str = 'Real', **kw):

        params = ParaMode(pat=pattern, mode=type)
        pattern, type = params.pat, params.mode

        if pattern in ['mul']:
            low, high = base*low, base*high
        else:
            low, high = base+low, base+high

        return getattr(space, type)(low=low, high=high, prior=self.config['prior'], transform=self.config['transform'])

    def tell(self, x, y, fit=True) -> OptimizeResult:
        """
        Feed data.

        Args:
            x ([type]): variable value.
            y ([type]): cost variable
            fit (bool, optional): fitting model. Defaults to True.

        Returns:
            OptimizeResult: current ans
        """
        return self.opt.tell(x, y, fit=fit)

    def ask(self, n_points=None, strategy="cl_min"):
        """
        Ask the next point to estimate.

        Args:
            n_points ([type], optional): n points. Defaults to None.
            strategy (str, optional): Defaults to "cl_min".
        """
        return self.opt.ask(n_points=n_points, strategy=strategy)

    def check(self, tol: float) -> bool:
        """
        Check whether the current result is less than the threshold.

        Args:
            tol (float): [description]

        Returns:
            bool: [description]
        """
        result = self.result()
        return result.fun < tol

    def result(self) -> OptimizeResult:
        """
        Get result.

        Returns:
            OptimizeResult: current result.
        """
        return self.opt.get_result()

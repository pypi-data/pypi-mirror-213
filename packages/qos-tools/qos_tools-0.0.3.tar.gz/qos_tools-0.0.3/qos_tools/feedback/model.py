# Author: Liu Pei  <liupei200546@163.com>  2021/10/13

from abc import abstractmethod

from scipy.optimize import OptimizeResult
from waveforms.scan_iter import OptimizerConfig

class FeedAgent(object):
    """
    Agent for feedback measurement.
    """

    config = []

    def __init__(self, variable: list[dict], *args, **kwds):
        pass

    @abstractmethod
    def tell(self, x, y) -> OptimizeResult:
        raise NotImplementedError()

    @abstractmethod
    def ask(self):
        raise NotImplementedError()

    @abstractmethod
    def check(self):
        raise NotImplementedError()

    @abstractmethod
    def get_result(self) -> OptimizeResult:
        raise NotImplementedError()

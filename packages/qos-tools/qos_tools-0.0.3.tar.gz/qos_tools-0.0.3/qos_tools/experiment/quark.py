# Author: Liu Pei  <liupei200546@163.com>  2021/08/14

import kernel
from qos_tools.experiment.scanner import Scanner


def quark_backend(**kw):

    task = kernel.create_task(Scanner, args=(), kwds=kw['init'])
    task.init(**kw)
    _task = kernel.submit(task)

    return _task

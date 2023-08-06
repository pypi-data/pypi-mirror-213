# Author: lizhiyuan  <lizhiyuan@baqis.ac.cn>  2021/01/01

import asyncio
import functools
from collections.abc import Awaitable
from qurpc.client import ZMQRPCCallable


__all__ = [
    'asyncmethod', 'ensure_awaitable', 'seq_exe', 'sync_exe',
]


async def asyncmethod(loop, func, *args, **kw):
    if asyncio.iscoroutinefunction(func):
        result = await func(*args, **kw)
    elif isinstance(func, ZMQRPCCallable):
        result = func(*args, **kw)
        if isinstance(result, Awaitable):
            result = await result
    else:
        result = await loop.run_in_executor(
            None, functools.partial(func, *args, **kw))
        if isinstance(result, Awaitable):
            result = await result
    return result


async def ensure_awaitable(func, *args, **kw):
    if asyncio.iscoroutinefunction(func):
        result = await func(*args, **kw)
    else:
        result = func(*args, **kw)
        if isinstance(result, Awaitable):
            result = await result
    return result


async def seq_exe(taskdict):
    '''顺序执行一个任务列表'''
    res = {}
    for k, task in taskdict.items():
        r = await task
        res.update({k: r})
    return res


async def sync_exe(taskdict):
    '''同步执行一个任务列表'''
    rl = await asyncio.gather(*taskdict.values())
    res = dict(zip(taskdict.keys(), rl))
    return res

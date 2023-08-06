# Author: lizhiyuan  <lizhiyuan@baqis.ac.cn>  2021/07/31

import itertools
import numpy as np

def CartesianSweepIterator(sweep_config={}, sweep_setting={}):
    '''Cartesian迭代函数，返回一个生成器

    Parameters:
        sweep_config: sweep_setting里key和其对应的地址以及额外的其他参数等，
            比如，{
                'name': 'S21',
                'Time': {
                    'addr': 'cfg.Q1.Gate.width',
                    'unit': 'a.u.'
                },
                'Amplitude': {
                    'addr': 'cfg.Q1.Gate.amp',
                    'unit': 'a.u.'
                },
            }
        sweep_setting: 
            比如，{
                'Time': np.linspace(0,3,4),
                'Amplitude': np.linspace(0,3,4),
            }
    '''
    for arg in itertools.product(*sweep_setting.values()):
        para_dict = {sweep_config[k]['addr']: v for k,
                   v in zip(sweep_setting.keys(), arg)}
        yield para_dict
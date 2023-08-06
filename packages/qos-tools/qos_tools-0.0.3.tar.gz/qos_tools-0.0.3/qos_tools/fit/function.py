# Author: lizhiyuan  <lizhiyuan@baqis.ac.cn>  2021/01/01

import numpy as np


def _T1(t, A, B, T1):
    y = A*np.exp(-t/T1)+B
    return y


def _Rabi(t, A, B, phi, Omega, Tr):
    y = A*np.exp(-t/Tr)*np.cos(2*np.pi*Omega*t+phi)+B
    return y


def _Ramsey(t, A, B, phi, T1, Tphi, Delta):
    y = A*np.exp(-t/2/T1-np.square(t/Tphi))*np.cos(2*np.pi*Delta*t+phi)+B
    return y


def _Ramsey_withBeat(t, A, B, phi, T1, Tphi, Delta, phi2, Delta2):
    y = A*np.exp(-t/2/T1-np.square(t/Tphi))*np.cos(
        2*np.pi*Delta*t+phi)*np.cos(2*np.pi*Delta2*t+phi2)+B
    return y


def _RB(t, A, B, p):
    y = A*p**t+B
    return y


def Linear(t, k, b):
    y = k * t + b
    return y


def Sin(t, A, B, f, phi):
    y = A*np.sin(2*np.pi*f*t+phi)+B
    return y


def Cauchy(t, A, t0, FWHM):
    y = A*FWHM/((t-t0)**2+FWHM**2)/np.pi
    return y


def Gaussian(x, A, miu, sigma):
    return A*np.exp(-((x-miu)/sigma)**2/2)


def F_ge(I, F_ge_max, Period, I_SS, d):
    '''
    基态和第一激发态能级间距与磁通偏置电流的关系
    F_ge是指基态和第一激发态能级间距

    I：偏置电流大小
    F_ge_max: 最高点频率，
    Period: 对应一个磁通量子的电流周期，
    I_SS: 频率最高点对应的电流大小，
    d: SQUID双结的不对称度参数，完全对称为0，完全不对称为1,
    '''
    phi = np.pi * (I - I_SS) / Period
    y = F_ge_max * (np.cos(phi)**2 + d * d * np.sin(phi)**2)**0.25
    return y


def F_cav(I, F_cav_bare, g_qr, F_ge_max, Period, I_SS, d):
    '''
    色散区域的谐振腔频率与磁通偏置电流的关系
    F_cav是谐振腔频率

    I：偏置电流大小
    F_cav_bare: 裸腔频率，
    g_qr: 谐振腔与量子比特的耦合常量，
    F_ge_max: 最高点频率，
    Period: 对应一个磁通量子的电流周期，
    I_SS: 频率最高点对应的电流大小，
    d: SQUID双结的不对称度参数，完全对称为0，完全不对称为1,
    '''
    F_ge_i = F_ge(I, F_ge_max, Period, I_SS, d)
    term1 = (F_cav_bare + F_ge_i)/2
    term2 = np.sqrt(g_qr * g_qr + (F_ge_i - F_cav_bare)**2 / 4)
    a = np.where(F_cav_bare > F_ge_i, 1, -1)
    y = term1 + term2*a
    return y

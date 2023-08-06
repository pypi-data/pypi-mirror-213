# Author: lizhiyuan  <lizhiyuan@baqis.ac.cn>  2021/01/29


import numpy as np
import matplotlib.pyplot as plt


def T1(fit, ax=None):
    ax = plt.gca() if ax is None else ax
    ax.set_xlabel(r'Time ($\mu$s)', fontsize=5)
    ax.set_ylabel('Ampitude', fontsize=5)
    ax.set_title('Energy Relaxation', fontsize=5)
    ax.text(0.95, 0.95, '$T_1\ =\ %.1f(%.2f)\ \mu$s' % (fit.params['T1'], fit.error['T1']),
             horizontalalignment='right', verticalalignment='top', transform=ax.transAxes, fontsize=5)


def Rabi(fit, ax=None):
    ax = plt.gca() if ax is None else ax
    ax.set_xlabel(r'Time ($\mu$s)', fontsize=5)
    ax.set_ylabel('Ampitude', fontsize=5)
    ax.set_title('Rabi', fontsize=5)
    ax.text(0.95, 0.95, '''$T_r\ =\ %.1f\ \mu$s
                            $\Omega\ =\ %.3f$ MHz
                            $pplen\ =\ %.4f a.u.$''' % (
        fit.params['Tr'], fit.params['Omega'], fit.params['pplen']),
        horizontalalignment='right', verticalalignment='top', transform=ax.transAxes, fontsize=5)


def Ramsey(fit, ax=None):
    ax = plt.gca() if ax is None else ax
    ax.set_xlabel(r'Time ($\mu$s)', fontsize=5)
    ax.set_ylabel('Ampitude', fontsize=5)
    ax.set_title('Ramsey', fontsize=5)
    ax.text(0.95, 0.95, '''$T_{1}\ =\ %.1f\ \mu$s
                            $T_{2}^{\star}\ =\ %.1f\ \mu$s
                            $T_{\phi}\ =\ %.1f(%.2f)\ \mu$s
                            $\Delta\ =\ %.4f$ MHz''' % (
        fit.params['T1'], fit.params['T2star'], fit.params['Tphi'], fit.error['Tphi'], fit.params['Delta']),
        horizontalalignment='right', verticalalignment='top', transform=ax.transAxes, fontsize=5)


def Ramsey_withBeat(fit, ax=None):
    ax = plt.gca() if ax is None else ax
    ax.set_xlabel(r'Time ($\mu$s)', fontsize=5)
    ax.set_ylabel('Ampitude', fontsize=5)
    ax.set_title('Ramsey_withBeat', fontsize=5)
    ax.text(0.95, 0.95, '''$T_{1}\ =\ %.1f\ \mu$s
                            $T_{2}^{\star}\ =\ %.1f\ \mu$s
                            $T_{\phi}\ =\ %.1f(%.2f)\ \mu$s
                            $\Delta\ =\ %.4f$ MHz
                            $\Delta_2\ =\ %.4f$ MHz''' % (
        fit.params['T1'], fit.params['T2star'], fit.params['Tphi'], fit.error['Tphi'], fit.params['Delta'], fit.params['Delta2']),
        horizontalalignment='right', verticalalignment='top', transform=ax.transAxes, fontsize=5)


def SpinEcho(fit, ax=None):
    ax = plt.gca() if ax is None else ax
    ax.set_xlabel(r'Time ($\mu$s)', fontsize=5)
    ax.set_ylabel('Ampitude', fontsize=5)
    ax.set_title('SpinEcho', fontsize=5)
    ax.text(0.95, 0.95, '''$T_{1}\ =\ %.1f\ \mu$s
                            $T_{2E}\ =\ %.1f\ \mu$s
                            $T_{\phi}\ =\ %.1f(%.2f)\ \mu$s
                            $\Delta\ =\ %.4f$ MHz''' % (
        fit.params['T1'], fit.params['T2E'], fit.params['Tphi'], fit.error['Tphi'], fit.params['Delta']),
        horizontalalignment='right', verticalalignment='top', transform=ax.transAxes, fontsize=5)


def RB(fit, ax=None):
    ax = plt.gca() if ax is None else ax
    ax.set_xlabel(r'Gate Number', fontsize=5)
    ax.set_ylabel('Ampitude', fontsize=5)
    ax.set_title('Randomized Benchmarking', fontsize=5)
    ax.text(0.95, 0.95, '''$p\ =\ %.4f(%.5f)$
                            $F\ =\ %.4f$''' % (
        fit.params['p'], fit.error['p'],fit.params['Fidelity']),
        horizontalalignment='right', verticalalignment='top', transform=ax.transAxes, fontsize=5)

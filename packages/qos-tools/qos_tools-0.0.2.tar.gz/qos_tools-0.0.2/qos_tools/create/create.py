# Author: Liu Pei  <liupei200546@163.com>  2021/08/14

from typing import Any, Literal, Optional


def create_dev(driver: Optional[str] = None, addr: Optional[str] = None, type: Literal['driver', 'remote'] = 'driver', srate: float = -1, **kw) -> dict:
    """
    Quick method for create a dev isinstance.

    Args:
        driver (Optional[str], optional): driver name. Defaults to None.
        addr (Optional[str], optional): address. Defaults to None.
        type (Literal[, optional): backend type. Defaults to 'driver'.
        srate (float, optional): sample rate. Defaults to -1.

    Returns:
        dict: keys to be completed.
    """
    return {
        "addr": addr,
        "name": driver,
        "type": type,
        "srate": srate,
    }


def add_setting(setting_LO: Optional[None] = None, setting_POW: Optional[float] = None, setting_OFFSET: Optional[float] = None, **kw) -> dict:
    """
    Quick method for add a `Setting` session.

    Args:
        setting_LO (Optional[None], optional): local frequency. Defaults to None.
        setting_POW (Optional[float], optional): power. Defaults to None.
        setting_OFFSET (Optional[float], optional): offset. Defaults to None.

    Returns:
        dict: keys to be completed.
    """
    return {
        "LO": setting_LO,
        "POW": setting_POW,
        "OFFSET": setting_OFFSET,  # 基本不用
    }


def add_waveform(waveform_SR: Optional[float] = None, waveform_LEN: Optional[float] = None, waveform_DDS_LO: Optional[float] = None, **kw) -> dict:
    """
    Quick method for add a `waveform` session.

    Args:
        waveform_SR (Optional[float], optional): sample rate for waveform. Defaults to None.
        waveform_LEN (Optional[float], optional): length for waveform. Defaults to None.
        waveform_DDS_LO (Optional[float], optional): DDS or Tek70000 local frequency. Defaults to None.

    Returns:
        dict: keys to be completed.
    """
    return {
        "SR": waveform_SR,
        "LEN": waveform_LEN,
        "DDS_LO": waveform_DDS_LO,
        "SW": "zero()",
        "TRIG": "zero()",
        "RF": "zero()",
        "Z": "zero()",
    }


def add_channel(channel_I: Optional[str] = None, channel_Q: Optional[str] = None, channel_LO: Optional[str] = None,
                channel_DDS: Optional[str] = None, channel_SW: Optional[str] = None, channel_TRIG: Optional[str] = None,
                channel_Z: Optional[str] = None, **kw) -> dict:
    """
    Quick method for add a `channel` session.

    Args:
        channel_I (Optional[str], optional): I channel equipment. Defaults to None.
        channel_Q (Optional[str], optional): Q channel equipment. Defaults to None.
        channel_LO (Optional[str], optional): local channel equipment. Defaults to None.
        channel_DDS (Optional[str], optional): DDS or Tek70000 channel equipment. Defaults to None.
        channel_SW (Optional[str], optional): swich channel equipment. Defaults to None.
        channel_TRIG (Optional[str], optional): trig channel equipment. Defaults to None.
        channel_Z (Optional[str], optional): Z channel equipment. Defaults to None.

    Returns:
        dict: keys to be completed.
    """
    return {
        "I": channel_I,
        "Q": channel_Q,
        "LO": channel_LO,
        "DDS": channel_DDS,
        "SW": channel_SW,
        "TRIG": channel_TRIG,
        "Z": channel_Z,
    }


def add_calibration_channel(delay: float = 0, distortion: Any = None) -> dict:
    """
    Quick method for add a `calibration` session.

    Args:
        delay (float, optional): delay time. Defaults to 0.
        distortion (Any, optional): method for distortion. Defaults to 0.

    Returns:
        dict: keys to be completed.
    """
    return {
        "delay": delay,
        "distortion": distortion,
    }


def add_calibration(calibration_I_delay: float = 0, calibration_I_distortion: Any = None, calibration_Q_delay: float = 0, calibration_Q_distortion: Any = None,
                    calibration_Z_delay: float = 0, calibration_Z_distortion: Any = None, calibration_DDS_delay: float = 0, calibration_DDS_distortion: Any = None,
                    calibration_TRIG_delay: float = 0, calibration_TRIG_distortion: Any = None, **kw) -> dict:
    """
    Quick method for add a `calibration` instance.

    Args:
        ref to `add_calibration_channel`.

    Returns:
        dict: keys to be completed.
    """
    return {
        "I": add_calibration_channel(calibration_I_delay, calibration_I_distortion),
        "Q": add_calibration_channel(calibration_Q_delay, calibration_Q_distortion),
        "Z": add_calibration_channel(calibration_Z_delay, calibration_Z_distortion),
        "DDS": add_calibration_channel(calibration_DDS_delay, calibration_DDS_distortion),
        "TRIG": add_calibration_channel(calibration_TRIG_delay, calibration_TRIG_distortion)
    }


def create_qubit(probe: Optional[str] = None, couplers: list[str] = [], **kw) -> dict:
    """
    Quick method for create a qubit isinstance.

    Args:
        probe (Optional[str], optional): probe name. Defaults to None.
        couplers (list[str], optional): couplers. Defaults to [].

    Returns:
        dict: keys to be completed.
    """
    return {
        "probe": probe,
        "couplers": couplers,
        "setting": add_setting(**kw),
        "waveform": add_waveform(**kw),
        "channel": add_channel(**kw),
        "calibration": add_calibration(**kw),
    }


def create_coupler(qubits: list[str] = [], **kw) -> dict:
    """
    Quick method for create a coupler isinstance.

    Args:
        qubits (list[str], optional): qubit list. Defaults to [].

    Returns:
        dict: keys to be completed.
    """
    return {
        "qubits": qubits,
        "setting": add_setting(**kw),
        "waveform": add_waveform(**kw),
        "channel": add_channel(**kw),
        "calibration": add_calibration(**kw),
    }


def create_probe(qubits: list[str] = [], adcsr: Optional[float] = None, channel_ADC: Optional[str] = None, pointNum: int = 2048, **kw) -> dict:
    """
    Quick method for create a probe isinstance.

    Args:
        qubits (list[str], optional): qubit list. Defaults to [].
        adcsr (Optional[float], optional): sample rate for adc. Defaults to None.
        channel_ADC (Optional[str], optional): ADC channel. Defaults to None.
        setting_SHOT (int, optional): repeat shots. Defaults to 1024.

    Returns:
        dict: keys to be completed.
    """

    setting = add_setting(**kw)
    setting.pop('OFFSET')
    setting['SHOT'] = 1024
    setting['TRIGD'] = 0
    setting['PNT'] = pointNum

    channel = add_channel(**kw)
    channel["ADC"] = channel_ADC

    return {
        "qubits": qubits,
        "adcsr": adcsr,
        "setting": setting,
        "waveform": add_waveform(**kw),
        "channel": channel,
        "calibration": add_calibration(**kw),
    }


def create_gate_measure(measure_frequency: Optional[float] = None, measure_duration: Optional[float] = None, measure_amp: Optional[float] = None,
                        measure_phi: float = 0, measure_threshold: float = 0, measure_type: str = "default", measure_bias: float = 0, **kw) -> dict:
    """
    Quick method for create a gate.Measure isinstance.

    Args:
        measure_frequency (Optional[float], optional): readout frequency. Defaults to None.
        measure_duration (Optional[float], optional): readout duration. Defaults to None.
        measure_amp (Optional[float], optional): [description]. readout amplitude to None.
        measure_phi (float, optional): svm add parameters. Defaults to 0.
        measure_threshold (float, optional): svm add parameters. Defaults to 0.
        measure_type (str, optional): readout type. Defaults to "default".

    Returns:
        dict: keys to be completed.
    """
    return {
        "params": {
            "frequency": measure_frequency,
            "duration": measure_duration,
            "amp": measure_amp,
            "phi": measure_phi,
            "threshold": measure_threshold,
            "bias": measure_bias,
        },
        "default_type": measure_type
    }


def create_gate_rfUnitary(default_type: str = "default", rfUnitary_shape: str = "CosPulse", rfUnitary_frequency: Optional[float] = None,
                          rfUnitary_amp: list[list[float]] = [[0, 0.5], [0, 1]], rfUnitary_duration: list[list[float]] = [[0, 0.5], [20e-9, 20e-9]],
                          rfUnitary_phase: list[list[float]] = [[-1, 1], [-1, 1]],  rfUnitary_buffer: float = 0,
                          rfUnitary_alpha: float = 1, rfUnitary_beta: float = 0, rfUnitary_delta: float = 0, **kw):
    """
    Quick method for create a gate.rfUnitary isinstance.

    Args:
        rfUnitary_type (str, optional): rfUnitary type. Defaults to "default".
        rfUnitary_shape (str, optional): rfUnitary shape. Defaults to "CosPulse".
        rfUnitary_frequency (Optional[float], optional): rfUnitary frequency Defaults to None.
        rfUnitary_amp (list[list[float]], optional): rfUnitary amplitude. Defaults to [[0, 0.5], [0, 1]].
        rfUnitary_duration (list[list[float]], optional): rfUnitary duration. Defaults to [[0, 0.5], [20e-9, 20e-9]].
        rfUnitary_phase (list[list[float]], optional): rfUnitary phase. Defaults to [[-1, 1], [-1, 1]].
        rfUnitary_alpha (float, optional): rfUnitary DRAG alpha. Defaults to 1.
        rfUnitary_beta (float, optional): rfUnitary beta alpha. Defaults to 0.
        rfUnitary_delta (float, optional): rfUnitary delta alpha. Defaults to 0.

    Returns:
        dict: keys to be completed.
    """
    return {
        "default_type": default_type,
        "params": {
            "shape": rfUnitary_shape,
            "frequency": rfUnitary_frequency,
            "amp": rfUnitary_amp,
            "duration": rfUnitary_duration,
            "phase": rfUnitary_phase,
            "alpha": rfUnitary_alpha,
            "beta": rfUnitary_beta,
            "delta": rfUnitary_delta,
            "buffer": rfUnitary_buffer,
        },
    }


def create_gate_CR(default_type: str = "default", cr_duration: float = 1e-6, cr_edge_type: str = 'cos',
                   cr_edge: float = 20e-9, cr_amp1: float = 0.8, cr_amp2: float = 0, cr_drag: float = 0, cr_skew: float = 0,
                   cr_global_phase: float = 0,  cr_relative_phase: float = 0, cr_phi1: float = 0, cr_phi2: float = 0,
                   cr_buffer: float = 10e-9, **kw) -> dict:
    """
    Quick method for create a gate._CR isinstance.

    Args:
        default_type (str, optional): Type. Defaults to "default".
        cr_duration (float, optional): Duration. Defaults to 1e-6.
        cr_edge_type (str, optional): Edge type. Defaults to 'cos'.
        cr_edge (float, optional): Edge length. Defaults to 20e-9.
        cr_amp1 (float, optional): Control amplitude. Defaults to 0.8.
        cr_amp2 (float, optional): Target amplitude. Defaults to 0.
        cr_drag (float, optional): DRAG. Defaults to 0.
        cr_skew (float, optional): Skew. Defaults to 0.
        cr_global_phase (float, optional): Global phase. Defaults to 0.
        cr_relative_phase (float, optional): Relative phase. Defaults to 0.
        cr_phi1 (float, optional): Control phase. Defaults to 0.
        cr_phi2 (float, optional): Target Phase. Defaults to 0.
        cr_buffer (float, optional): Buffer. Defaults to 10e-9.

    Returns:
        dict: keys to be completed.
    """

    return {
        "default_type": default_type,
        "params": {
            "duration": cr_duration,
            "edge_type": cr_edge_type,
            "edge": cr_edge,
            "amp1": cr_amp1,
            "amp2": cr_amp2,
            "drag": cr_drag,
            "skew": cr_skew,
            "global_phase": cr_global_phase,
            "relative_phase": cr_relative_phase,
            "phi1": cr_phi1,
            "phi2": cr_phi2,
            "buffer": cr_buffer
        }
    }


def create_jpa() -> dict:
    pass


gate_mapping_1 = {
    'rfUnitary': create_gate_rfUnitary,
    'Measure': create_gate_measure,
}

gate_mapping_2 = {
    'CR': [('D', create_gate_CR)],
}

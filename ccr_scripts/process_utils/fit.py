import numpy as np
from scipy.optimize import curve_fit
from typing import Tuple, List, Union, Iterable


def estimate_acorr_fitting_limit(data: List[Union[float, int]],
                                 window_size=50,
                                 pos_diff_ratio=0.5,
                                 ) -> int:
    """
    Returns minimum of
    1) number of points at the beginning of `data` for which in every
    `window_size` range there are no more than `pos_diff_ratio` positive
    derivatives
    2) first data point which cross zero

    :param data: array of function values
    :param window_size: number of points in window
    :param pos_diff_ratio: allowed ratio of positive diff in window
    :return: index separates region with small
             amount of negative derivatives
    """

    def moving_average(data_set, periods=3):
        weights = np.ones(periods) / periods
        return np.convolve(data_set, weights, mode='valid')

    diff = np.diff(data)
    pos_diff = (diff > 0).astype(int)
    pos_diff_avg = moving_average(pos_diff, window_size)
    index = np.argmax(pos_diff_avg >= pos_diff_ratio) + window_size // 2
    if sum(pos_diff_avg) == 0.0:
        index = len(data)
    first_negative = np.array(data < 0).argmax()
    if data[first_negative] >= 0:
        first_negative = len(data)
    index = min(index, first_negative)
    return index


def __multi_exp_f(x: Union[float, int],
                  A: List[Union[float, int]],
                  TAU: List[Union[float, int]],
                  C: Union[float, int] = 0) -> float:
    """
    :param x: argument of some exponential functions composition
    :param A: array of amplitudes
    :param TAU: array of time constants
    :param C: free element
    :return: sum exponential functions composition
    """
    return sum(
        (a * np.exp(-x / tau)) for a, tau in zip(A, TAU)
    ) + C


def multi_exp_unfixed_amplitude(x: Union[float, int], *args):
    """
    :param x: argument of some exponential functions composition
    :param args: array of amplitudes and time constants
    :return: callable __multi_exp_f
    """
    TAU = list(args[1::2])

    if len(args) % 2 == 0:
        C = 0
        A = list(args[::2])
    else:
        C = args[-1]
        A = args[:-1:2]

    return __multi_exp_f(x, A, TAU, C)


def multi_exp_fixed_amplitude_1(x: Union[float, int], *args):
    """
    :param x: argument of some exponential functions composition
    :param args: array of amplitudes and time constants
    :return: callable __multi_exp_f
    """
    TAU = args[1::2]
    A = np.abs(args[::2]) / sum(args[::2])

    return __multi_exp_f(x, A, TAU)


def fit_corrfunc_amp_fixed_1(time: List[float],
                             acorr: List[float],
                             bounds: List[List[List[Union[float, int]]]]) \
        -> Union[np.ndarray, Iterable, int, float]:
    """
    Fit input data with :math:`\\sum_n A_n \\exp(-t/\\tau_n) + const`

    :param time: time data series
    :param acorr: auto-correlation data series
    :param bounds: curve parameters bounds
    :return: Fit curve parameters
    """

    p0 = np.mean(bounds, axis=0)

    args, pcov = curve_fit(multi_exp_fixed_amplitude_1,
                           time,
                           acorr,
                           p0=p0,
                           bounds=np.array(bounds))
    args[::2] = np.abs(args[::2]) / sum(args[::2])

    return list(args)


def fit_corrfunc_amp_unfixed(time: List[float],
                             acorr: List[float],
                             bounds: List[List[List[Union[float, int]]]]) \
        -> Union[np.ndarray, Iterable, int, float]:
    """
    Fit input data with :math:`\\sum_n A_n \\exp(-t/\\tau_n) + const`

    :param time: time data series
    :param acorr: auto-correlation data series
    :param bounds: curve parameters bounds
    :return: Fit curve parameters
    """

    p0 = np.mean(bounds, axis=0)

    args, pcov = curve_fit(multi_exp_unfixed_amplitude,
                           time,
                           acorr,
                           p0=p0,
                           bounds=np.array(bounds))

    return list(args)


def bounds_scaled_fit_auto_correlation(time: List[float],
                                       corr: List[float],
                                       bounds: List[List[Union[float, int]]],
                                       scales=None,
                                       fit_func=fit_corrfunc_amp_fixed_1
                                       ) \
        -> Tuple[int, Union[np.ndarray, Iterable, int, float]]:
    """
    Fit input data with :math:`\\sum_n A_n \\exp(-t/\\tau_n) + const`

    :param time: time data series
    :param corr: correlation data series
    :param bounds: curve parameters bounds
    :param scales: array of coefficients to scale boundaries
    :bounds_scaled_fit_auto_correlation: function for fit data with scaled bounds
    :return: Fit curve parameters
    """

    def scale_times(args, scale):
        args[1::2] = np.array(args[1::2]) * scale

    if scales is None:
        scales = [1, 1]

    R_square = []
    popt_all = []

    for i, scale in enumerate(scales):
        scale_times(bounds[0], scale)
        scale_times(bounds[1], scale)
        try:
            popt = fit_func(time, corr, bounds)
            R_square.append(sum((np.array(corr) - np.array(multi_exp_unfixed_amplitude(time, *popt))) ** 2))
            popt_all.append(popt)
        except RuntimeError:
            print("Fit error n={}, scale={}".format(len(bounds[0]) // 2, scale))

        scale_times(bounds[0], 1.0 / scale)
        scale_times(bounds[1], 1.0 / scale)

    min_ind_r_square = np.argmin(R_square)

    return popt_all[min_ind_r_square]

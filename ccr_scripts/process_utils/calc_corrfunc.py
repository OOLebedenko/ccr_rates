import numpy as np


def Y2m2(vectors):
    result = np.zeros(len(vectors), dtype=complex)
    coef = 1.0 / 4.0 * np.sqrt(15.0 / 2.0 / np.pi)

    return coef * (vectors[:, 0] - 1j * vectors[:, 1]) ** 2

def Y2m1(vectors):
    result = np.zeros(len(vectors), dtype=complex)
    coef = 1.0 / 2.0 * np.sqrt(15.0 / 2.0 / np.pi)

    return coef * (vectors[:,0] - 1j * vectors[:, 1]) * vectors[:, 2]


def Y20(vectors):
    result = np.zeros(len(vectors), dtype=complex)
    coef = 1.0 / 4.0 * np.sqrt(5.0 / np.pi)

    return coef * (2.0 * vectors[:, 2] ** 2 - vectors[:, 0] ** 2 - vectors[:, 1] ** 2)


def Y2p1(vectors):
    result = np.zeros(len(vectors), dtype=complex)
    coef = -1.0 / 2.0 * np.sqrt(15.0 / 2.0 / np.pi)

    return coef * (vectors[:, 0] + 1j * vectors[:, 1]) * vectors[:, 2]


def Y2p2(vectors):
    result = np.zeros(len(vectors), dtype=complex)
    coef = 1.0 / 4.0 * np.sqrt(15.0 / 2.0 / np.pi)

    return coef * (vectors[:,0] + 1j * vectors[:,1]) ** 2


def autocorr(x):
    # return real part of autocorrelation function
    f = np.fft.fft(np.pad(x, len(x), mode='constant'))
    result = np.fft.ifft(f * np.conj(f))
    result = result[:len(x)]
    result /= np.linspace(len(x), 1, len(x))
    return np.real(result)

def cross_correlation_using_fft(v1, v2):
    v1 = np.concatenate((v1, np.zeros(len(v1) - 1)))  # added zeros to signal
    v2 = np.concatenate((v2, np.zeros(len(v2) - 1)))  # added zeros to signal
    f1 = np.fft.fft(v1)
    f2 = np.fft.fft(v2)
    f2 = np.conj(f2)
    cc = np.real(np.fft.ifft(f1 * f2))
    cc[1:(cc.size // 2) + 1] += cc[(cc.size // 2) + 1:][::-1]
    cc[1:(cc.size // 2) + 1] /= 2
    cc = cc[:(cc.size // 2) + 1]

    return cc / np.linspace(len(cc), 1, len(cc))


def autocorr_all_harmonics(r):
    r = r / np.linalg.norm(r, axis=1)[:, np.newaxis]
    res = [cross_correlation_using_fft(f, f) for f in [Y2m2(r), Y2m1(r), Y20(r)]]
    res[0] = 2.0 * res[0]
    res[1] = 2.0 * res[1]
    return 4.0 * np.pi / 5.0 * np.sum(res, axis=0)


def crosscorr_all_harmonics(v1, v2):
    v1 = v1 / np.linalg.norm(v1, axis=1)[:, np.newaxis]
    v2 = v2 / np.linalg.norm(v2, axis=1)[:, np.newaxis]

    Y_func_v1 = [Y2m2(v1), Y2m1(v1), Y20(v1)]
    Y_func_v2 = [Y2m2(v2), Y2m1(v2), Y20(v2)]
    res = [cross_correlation_using_fft(f1, f2) for f1, f2 in zip(Y_func_v1, Y_func_v2)]
    res[0] = 2.0 * res[0]
    res[1] = 2.0 * res[1]
    return 4.0 * np.pi / 5.0 * np.sum(res, axis=0)


def crosscorr_all_harmonics_with_radial(v1, v2):
    norm_v1 = np.linalg.norm(v1, axis=1)
    norm_v2 = np.linalg.norm(v2, axis=1)
    v1 = v1 / norm_v1[:, np.newaxis]
    v2 = v2 / norm_v2[:, np.newaxis]

    Y_func_v1 = [Y2m2(v1), Y2m1(v1), Y20(v1)]
    Y_func_v2 = [Y2m2(v2), Y2m1(v2), Y20(v2)]
    res = [cross_correlation_using_fft(f1, f2) for f1, f2
           in zip(Y_func_v1 * norm_v1 ** (-3), Y_func_v2 * norm_v2 ** (-3))]

    res[0] = 2.0 * res[0]
    res[1] = 2.0 * res[1]
    return 4.0 * np.pi / 5.0 * np.sum(res, axis=0)

import numpy as np
from scipy.signal import morlet2
def compute_time_frequency(data, sfreq, freqs, method='morlet', n_cycles=7):
    """
    Compute time-frequency power using wavelet transform.

    Parameters:
        data (array-like): Input data.
        sfreq (float): Sampling frequency of the data.
        freqs (array-like): Frequencies of interest.
        method (str, optional): Wavelet method to use. Default is 'morlet'.
        n_cycles (int, optional): Number of cycles used in the wavelet. Default is 7.

    Returns:
        array-like: Time-frequency power array.

    """
    n_samples = len(data)
    time_bandwidth = 2 * n_cycles
    power = np.zeros((len(freqs), n_samples))
    for i, freq in enumerate(freqs):
        w = 2 * np.pi * freq
        wavelet = morlet2(n_samples, w, time_bandwidth)
        convolved = np.convolve(data, wavelet, mode='same')
        power[i, :] = np.abs(convolved)**2

    return power


def calculate_peak_frequency(psd, freqs):
    """
    Calculate the peak frequency for each power spectrum.

    Parameters:
        psd (array-like): Power spectrum array.
        freqs (array-like): Frequencies corresponding to the power spectrum.

    Returns:
        array-like: Peak frequency for each power spectrum.

    """
    peak_freqs = freqs[np.argmax(psd, axis=1)]
    return peak_freqs

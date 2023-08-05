import numpy as np
from scipy.stats import linregress

def calculate_multi_fractal_spectrum(eeg_data, q_values):
    """
    Calculates the multi-fractal spectrum for EEG data.

    Args:
        eeg_data (numpy.ndarray): EEG data array of shape (channels, samples).
        q_values (list): List of q values for which to calculate the spectrum.

    Returns:
        numpy.ndarray: Multi-fractal spectrum array of shape (2, len(q_values)),
                       where the first row corresponds to f(alpha) and the second
                       row corresponds to D(q).
    """
    # Calculate the wavelet leaders for each channel
    wavelet_leaders = []
    for channel in eeg_data:
        wavelet_coefficients = np.abs(np.fft.fft(channel)) ** 2
        wavelet_leaders.append(np.cumsum(wavelet_coefficients[::-1])[::-1])

    wavelet_leaders = np.array(wavelet_leaders)

    # Calculate the q-th order moments
    moments = []
    for q in q_values:
        moments.append(np.mean(wavelet_leaders ** q, axis=0))

    moments = np.array(moments)

    # Calculate the singularity spectrum
    f_alpha = []
    D_q = []
    for moment in moments:
        x = np.log(np.arange(1, len(moment)+1))
        # alpha, _, _, _, _ = linregress(x, np.log(moment))
        alpha, _, _, _, _ = linregress(np.log(np.arange(1, len(moment) + 1)), np.log(moment))

        f_alpha.append(alpha)
        D_q.append(alpha / (q_values - 1))

    spectrum = np.array([f_alpha, D_q])

    return spectrum

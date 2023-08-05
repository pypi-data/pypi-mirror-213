import pandas as pd
import numpy as np
from scipy import signal
from scipy.stats import pearsonr, spearmanr
from scipy.signal import correlate
import numpy as np
from sklearn.metrics import mutual_info_score

def calculate_interchannel_correlation(data):
    """
    Calculate the interchannel correlation matrix of the given data.

    Parameters:
        data (array-like): Input data with shape (n_samples, n_channels).

    Returns:
        array-like: Interchannel correlation matrix with shape (n_channels, n_channels).
    """
    correlation_matrix = np.corrcoef(data.T)
    return correlation_matrix

def calculate_correlation(data, method='pearson'):
    """
    Calculate the correlation matrix of the given data using the specified method.

    Parameters:
        data (DataFrame): Input data with shape (n_samples, n_channels).
        method (str): Correlation method to use. Options: 'pearson' (default), 'spearman'.

    Returns:
        DataFrame: Correlation matrix with shape (n_channels, n_channels).
    """
    if method == 'pearson':
        corr_matrix = pearsonr(data)
    elif method == 'spearman':
        corr_matrix = spearmanr(data)
    else:
        raise ValueError("Invalid correlation method. Must be 'pearson' or 'spearman'.")
    correlations = pd.DataFrame(corr_matrix[0], columns=data.columns[1:], index=data.columns[1:]) 
    return correlations

def calculate_cross_correlation(data1, data2):
    """
    Calculate the cross-correlation between two data sequences.

    Parameters:
        data1 (array-like): First data sequence.
        data2 (array-like): Second data sequence.

    Returns:
        array-like: Cross-correlation values.
        array-like: Lags corresponding to the cross-correlation values.
    """
    xcorr = correlate(data1, data2)
    lags = np.arange(-len(data1) + 1, len(data1))
    return xcorr, lags

def calculate_phase_sync(data1, data2):
    """
    Calculate the phase synchronization between two data sequences.

    Parameters:
        data1 (array-like): First data sequence.
        data2 (array-like): Second data sequence.

    Returns:
        float: Phase synchronization value.
    """
    phase_diff = np.angle(np.exp(1j * (np.angle(np.fft.fft(data1)) - np.angle(np.fft.fft(data2)))))
    return np.abs(np.mean(np.exp(1j * phase_diff)))

def calculate_mutual_information(x, y):
    """
    Calculate the mutual information between two data sequences.

    Parameters:
        x (array-like): First data sequence.
        y (array-like): Second data sequence.

    Returns:
        float: Mutual information value.
    """
    mi = mutual_info_score(x, y)
    return mi

def calculate_coherence(eeg_data, fs):
    """
    Calculate the coherence matrix of the given EEG data.

    Parameters:
        eeg_data (array-like): EEG data with shape (n_samples, n_channels).
        fs (float): Sampling frequency of the EEG data.

    Returns:
        array-like: Coherence matrix with shape (n_channels, n_channels).
    """
    n_channels = eeg_data.shape[1]
    coherence_matrix = np.zeros((n_channels, n_channels))
    for i in range(n_channels):
        for j in range(i + 1, n_channels):
            f, coherence = signal.coherence(eeg_data[:, i], eeg_data[:, j], fs=fs)
            avg_coherence = np.mean(coherence)
            coherence_matrix[i, j] = avg_coherence
            coherence_matrix[j, i] = avg_coherence

    return coherence_matrix

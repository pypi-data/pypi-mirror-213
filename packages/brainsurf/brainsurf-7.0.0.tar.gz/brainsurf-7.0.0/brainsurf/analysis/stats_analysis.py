import numpy as np
import pandas as pd
from scipy import signal
import numpy as np
import nolds

import numpy as np

def calculate_mean(data):
    return np.nanmean(data)

def calculate_variance(data):
    return np.nanvar(data)

def calculate_std(data):
    return np.nanstd(data)

def calculate_skewness(data):
    mean = np.nanmean(data)
    std = np.nanstd(data)
    skewness = np.nanmean(((data - mean) ** 3)) / (std ** 3)
    return skewness

def calculate_kurtosis(data):
    mean = np.nanmean(data)
    std = np.nanstd(data)
    kurtosis = np.nanmean(((data - mean) ** 4)) / (std ** 4)
    return kurtosis



def calculate_cohens_d(x1, x2):
    mean1, mean2 = np.mean(x1), np.mean(x2)
    std1, std2 = np.std(x1, ddof=1), np.std(x2, ddof=1)
    pooled_std = np.sqrt(((len(x1) - 1) * std1 ** 2 + (len(x2) - 1) * std2 ** 2) / (len(x1) + len(x2) - 2))
    cohens_d = (mean1 - mean2) / pooled_std
    return cohens_d

def calculate_coherence(data1, data2, fs):
    freqs, psd_data1 = signal.welch(data1, fs=fs, nperseg=1024)
    freqs, psd_data2 = signal.welch(data2, fs=fs, nperseg=1024)
    freqs, csd = signal.csd(data1, data2, fs=fs, nperseg=1024)
    coh = np.abs(csd)**2 / (psd_data1 * psd_data2)
    return freqs, coh


def calculate_max(data):
    return np.max(data, axis=1)

def calculate_min(data):
    return np.min(data, axis=1)

def calculate_relative_power(freqs, psd):
    delta_mask = (freqs >= 0.5) & (freqs <= 4)
    theta_mask = (freqs >= 4) & (freqs <= 8)
    alpha_mask = (freqs >= 8) & (freqs <= 13)
    beta_mask = (freqs >= 13) & (freqs <= 30)

    delta_power = np.trapz(psd[delta_mask], freqs[delta_mask])
    theta_power = np.trapz(psd[theta_mask], freqs[theta_mask])
    alpha_power = np.trapz(psd[alpha_mask], freqs[alpha_mask])
    beta_power = np.trapz(psd[beta_mask], freqs[beta_mask])

    total_power = delta_power + theta_power + alpha_power + beta_power

    delta_power=delta_power / total_power
    theta_power=theta_power / total_power
    alpha_power=alpha_power / total_power
    beta_power=beta_power / total_power
    return {
        "delta": delta_power / total_power,
        "theta": theta_power / total_power,
        "alpha": alpha_power / total_power,
        "beta": beta_power / total_power
    }

def calc_ap_entropy(data, m=2, r=0.2):
    ae = nolds.sampen(data, emb_dim=m, tolerance=r)
    return ae

def calc_fractal_dimension(data):
    fd = nolds.dfa(data)
    return fd

import scipy.stats as stats

def perform_ttest(df1, df2, column):
    """
    Perform a t-test on two dataframes for a given column.

    Arguments:
    df1 -- First dataframe
    df2 -- Second dataframe
    column -- Column name for the t-test

    Returns:
    t_value -- T-statistic
    p_value -- Two-tailed p-value
    """
    # Select the column data from the dataframes
    data1 = df1[column]
    data2 = df2[column]

    # Perform t-test
    t_value, p_value = stats.ttest_ind(data1, data2)

    return t_value, p_value

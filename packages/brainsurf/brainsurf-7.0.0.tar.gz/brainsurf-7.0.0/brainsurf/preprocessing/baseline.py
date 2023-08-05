import numpy as np
from sklearn.decomposition import PCA
import pandas as pd

def apply_baseline_correction(epochs, fs):
    """
    Apply baseline correction to the epochs.

    Parameters:
        epochs (ndarray): Epochs data of shape (n_epochs, n_channels, n_samples).
        fs (float): Sampling frequency of the data.

    Returns:
        ndarray: Baseline-corrected epochs data.
    """
    baseline_duration = 0.5 
    num_samples = int(baseline_duration * fs)
    baseline_mean = np.mean(epochs[:, :num_samples], axis=1, keepdims=True)
    baseline_corrected_epochs = epochs - baseline_mean
    return baseline_corrected_epochs


def compute_mean_baseline(data, sfreq, baseline=(None, 0)):
    """
    Compute the mean baseline of the data.

    Parameters:
        data (ndarray): Data array of shape (n_channels, n_samples).
        sfreq (float): Sampling frequency of the data.
        baseline (tuple): Start and end time of the baseline period in seconds (default: (None, 0)).

    Returns:
        ndarray: Mean baseline of each channel.
    """
    if baseline[0] is None:
        start = 0
    else:
        start = int(round(baseline[0] * sfreq))
    if baseline[1] is None:
        end = data.shape[1]
    else:
        end = int(round(baseline[1] * sfreq))

    baseline_data = data[:, start:end]
    baseline_mean = np.mean(baseline_data, axis=1)

    return baseline_mean


def apply_baseline(data, sfreq, baseline=(None, 0)):
    """
    Apply baseline correction to the data.

    Parameters:
        data (ndarray): Data array of shape (n_channels, n_samples).
        sfreq (float): Sampling frequency of the data.
        baseline (tuple): Start and end time of the baseline period in seconds (default: (None, 0)).

    Returns:
        ndarray: Baseline-corrected data.
    """
    baseline_mean = compute_mean_baseline(data, sfreq, baseline)
    data_bc = data - baseline_mean[:, np.newaxis]
    return data_bc


def extract_features(epochs):
    """
    Extract features from epochs.

    Parameters:
        epochs (ndarray): Epochs data of shape (n_epochs, n_channels, n_samples).

    Returns:
        ndarray: Extracted features.
    """
    features = np.mean(epochs, axis=1)  # Placeholder, implement as required
    return features


def normalize_features(features):
    """
    Normalize the features.

    Parameters:
        features (ndarray): Features array.

    Returns:
        ndarray: Normalized features.
    """
    normalized_features = (features - np.mean(features)) / np.std(features)
    return normalized_features


def reduce_dimensionality(features):
    """
    Reduce the dimensionality of the features using PCA.

    Parameters:
        features (ndarray): Features array.

    Returns:
        ndarray: Reduced-dimensional features.
    """
    num_components = 10  # Number of components to retain
    pca = PCA(n_components=num_components)
    reduced_features = pca.fit_transform(features)
    return reduced_features



def perform_pca_df(data, num_components):
    """
    Perform dimension reduction using Principal Component Analysis (PCA).
    
    Args:
    - data (pandas.DataFrame): The input data dataframe with shape (n_samples, n_features).
    - num_components (int): The number of components (principal axes) to retain.
    
    Returns:
    - reduced_data (pandas.DataFrame): The reduced data dataframe with shape (n_samples, num_components).
    - pca (sklearn.decomposition.PCA): The fitted PCA object.
    """
    pca = PCA(n_components=num_components)
    reduced_data = pca.fit_transform(data)
    column_names = [f"Component {i+1}" for i in range(num_components)]
    reduced_data = pd.DataFrame(reduced_data, columns=column_names)
    return reduced_data, pca

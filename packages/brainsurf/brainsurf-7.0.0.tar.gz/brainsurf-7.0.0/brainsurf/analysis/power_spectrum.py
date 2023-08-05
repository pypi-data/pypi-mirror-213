import numpy as np
from scipy.signal import welch, coherence, correlate
import astropy as ast 
from scipy import signal

# def extract_frequency_bands(raw_data, fs=128):
#     epoch_length = 1000  # Length of each epoch in milliseconds
#     num_epochs = len(raw_data) // epoch_length
#     pre_epochs = np.split(raw_data[:num_epochs * epoch_length], num_epochs)
    
#     # Initialize the dictionary to store the frequency bands
#     data = {}
    
#     for band in ['alpha', 'beta', 'delta', 'theta', 'gamma']:
#         if band not in data:
#             pre_features = []
            
#             for epoch in pre_epochs:
#                 f, psd = welch(epoch, fs=fs)
                
#                 # Adjust the frequency range based on the band
#                 if band == 'alpha':
#                     band_psd = psd[(f >= 8) & (f <= 13)]
#                 elif band == 'beta':
#                     band_psd = psd[(f >= 13) & (f <= 30)]
#                 elif band == 'delta':
#                     band_psd = psd[(f >= 1) & (f <= 4)]
#                 elif band == 'theta':
#                     band_psd = psd[(f >= 4) & (f <= 8)]
#                 elif band == 'gamma':
#                     band_psd = psd[(f >= 30) & (f <= 50)]
#                 else:
#                     raise ValueError("Invalid frequency band.")
#                 band_power = np.mean(band_psd) if band_psd.any() else np.nan
#                 pre_features.append(band_power)
            
#             # Make sure the extracted features have the same length as the original data
#             pre_features += [np.nan] * (len(raw_data) - len(pre_features))
            
#             data[band] = pre_features
            
#     return data
import pandas as pd
import numpy as np
from scipy.signal import welch

def extract_frequency_bands(raw_data, fs=128):
    epoch_length = 1000  # Length of each epoch in milliseconds
    num_epochs = len(raw_data) // epoch_length
    pre_epochs = np.split(raw_data.values[:num_epochs * epoch_length, :-2], num_epochs)

    # Initialize the dictionary to store the frequency bands for each channel
    data = {}

    for channel in range(raw_data.shape[1] - 2):
        channel_data = raw_data.iloc[:, channel]
        channel_features = {}

        for band in ['alpha', 'beta', 'delta', 'theta', 'gamma']:
            if band not in channel_features:
                pre_features = []

                for epoch in pre_epochs:
                    f, psd = welch(epoch[:, channel], fs=fs)

                    # Adjust the frequency range based on the band
                    if band == 'alpha':
                        band_psd = psd[(f >= 8) & (f <= 13)]
                    elif band == 'beta':
                        band_psd = psd[(f >= 13) & (f <= 30)]
                    elif band == 'delta':
                        band_psd = psd[(f >= 1) & (f <= 4)]
                    elif band == 'theta':
                        band_psd = psd[(f >= 4) & (f <= 8)]
                    elif band == 'gamma':
                        band_psd = psd[(f >= 30) & (f <= 50)]
                    else:
                        raise ValueError("Invalid frequency band.")

                    band_power = np.mean(band_psd) if band_psd.any() else np.nan
                    pre_features.append(band_power)

                # Make sure the extracted features have the same length as the original data
                pre_features += [np.nan] * (len(raw_data) - len(pre_features))

                channel_features[band] = pre_features

        data[channel] = channel_features

    # Convert the extracted frequency bands dictionary to a DataFrame
    frequency_bands_df = pd.DataFrame(data)
    
    return frequency_bands_df


def psd_fft(data, sfreq, freq_range=(0, 100)):
    fft_data = np.fft.rfft(data)
    power_spectrum = np.abs(fft_data)**2 / len(data)
    freqs = np.fft.rfftfreq(len(data), 1.0/sfreq)
    mask = (freqs >= freq_range[0]) & (freqs <= freq_range[1])
    freqs = freqs[mask]
    power_spectrum = power_spectrum[mask]
    return freqs, power_spectrum

def psd_welch(data, fs):
    nperseg= calculate_nperseg(data)
    freqs, psd = welch(data, fs=fs, nperseg=10)
    print(freqs)
    return freqs, psd

def psd_lombscargle(signal, fs):
    time = np.arange(len(signal))/fs
    frequency, power = ast.timeseries.LombScargle(time, signal).autopower(normalization='psd')
    return frequency, power

def calculate_psd(data, sfreq):
    freqs, psd = signal.welch(data, sfreq, nperseg=512)
    return psd, freqs

def calculate_power_within_bands(psd, freqs):
    frequency_bands = {
    'Delta': (0.5, 4),
    'Theta': (4, 8),
    'Alpha': (8, 12),
    'Beta': (12, 30)
}
    num_channels = psd.shape[0]
    power_within_bands = {}

    for channel in range(num_channels):
        power_within_bands[channel] = {}

        for band_name, frequency_range in frequency_bands.items():
            freq_indices = np.where(np.logical_and(freqs >= frequency_range[0], freqs <= frequency_range[1]))
            power_within_band = np.trapz(psd[channel, freq_indices], freqs[freq_indices])
            power_within_bands[channel][band_name] = power_within_band

    return power_within_bands

def calculate_overlapping_percentage(power_within_bands):
    num_channels = len(power_within_bands)
    overlapping_percentage = {}

    for channel in power_within_bands.keys():
        overlapping_percentage[channel] = {}

        for band_name, band_power in power_within_bands[channel].items():
            total_power = np.sum(list(power_within_bands[channel].values()))
            percentage = band_power / total_power * 100
            overlapping_percentage[channel][band_name] = percentage

    overlapping_df = pd.DataFrame.from_dict(overlapping_percentage)
    return overlapping_df


def calculate_nperseg(data):
    n = len(data)
    if n < 256:
        nperseg = n
    elif n < 2048:
        nperseg = 256
    else:
        nperseg = 1024
    return nperseg
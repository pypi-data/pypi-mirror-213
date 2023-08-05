import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import spectrogram


def plot_spectrogram(data, fs, window='hann',nperseg=256, noverlap=None, cmap='RdBu_r', show=True,scaling='density',):
    f, t, Sxx = spectrogram(data, fs=fs, window=window, nperseg=nperseg, noverlap=noverlap, scaling=scaling)
    plt.pcolormesh(t, f, Sxx, cmap=cmap)
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Time [sec]')
    plt.colorbar()
    plt.show()
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.signal import spectrogram
from scipy.signal import coherence
from scipy.signal import correlate2d

class EEGVisualizationFactory:
    def __init__(self, data):
        self.data = data

    def plot_eeg_signal(self, x_label='Time [sec]', y_label='EEG', title='EEG Signal'):
        sec = self.data['sec']
        eeg = self.data['raw']
        plt.plot(sec, eeg)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.title(title)
        plt.show()

    def plot_spectrogram(self, channel, fs=None, window='hann', nperseg=256, noverlap=None,
                         cmap='RdBu_r', scaling='density', x_label='Time [sec]', y_label='Frequency [Hz]',
                         title=None):
        sec = self.data['sec']
        channel_data = self.data[channel]
        if fs is None:
            fs = 1.0 / (sec[1] - sec[0])
        f, t, Sxx = spectrogram(channel_data, fs=fs, window=window, nperseg=nperseg, noverlap=noverlap, scaling=scaling)
        plt.pcolormesh(t, f, Sxx, cmap=cmap)
        plt.ylabel(y_label)
        plt.xlabel(x_label)
        if title is not None:
            plt.title(title)
        else:
            plt.title(f'Spectrogram ({channel})')
        plt.colorbar()
        plt.show()

    def plot_power_spectrum(self, channel, fs=None, x_label='Frequency [Hz]', y_label='Power Spectral Density',
                            title=None):
        sec = self.data['sec']
        channel_data = self.data[channel]
        if fs is None:
            fs = 1.0 / (sec[1] - sec[0])
        f, Pxx = plt.psd(channel_data, Fs=fs)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        if title is not None:
            plt.title(title)
        else:
            plt.title(f'Power Spectrum ({channel})')
        plt.show()

    def plot_coherence(self, channel1, channel2, freq_range=None):
        sec = self.data['sec']
        data1 = self.data[channel1]
        data2 = self.data[channel2]
        fs = 1.0 / (sec[1] - sec[0])
        f, Cxy = coherence(data1, data2, fs=fs)

        if freq_range is not None:
            mask = (f >= freq_range[0]) & (f <= freq_range[1])
            f = f[mask]
            Cxy = Cxy[mask]

        df = pd.DataFrame({'frequency': f, 'coherence': Cxy})
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.lineplot(x='frequency', y='coherence', data=df, ax=ax)
        ax.set_title('Coherence Plot')
        ax.set_xlabel('Frequency (Hz)')
        ax.set_ylabel('Coherence')
        plt.show()

    def plot_cross_correlation(self, channel1, channel2):
        data1 = self.data[channel1]
        data2 = self.data[channel2]
        corr = np.correlate(data1, data2, mode='same')
        plt.plot(corr)
        plt.xlabel('Time')
        plt.ylabel('Cross-Correlation')
        plt.title(f'Cross-Correlation ({channel1} vs {channel2})')
        plt.show()

    def plot_heatmap(self):
        eeg_df = pd.DataFrame(self.data)
        # Calculate the correlation matrix
        corr_matrix = eeg_df.corr()
        # Plot the correlation heatmap
        plt.figure(figsize=(10, 8))
        sns.heatmap(corr_matrix, cmap='RdBu_r', annot=True, fmt=".2f", vmin=-1, vmax=1)
        plt.title('EEG Data Heatmap')
        plt.xticks(rotation=90)
        plt.yticks(rotation=0)
        plt.show()






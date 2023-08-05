import numpy as np
import matplotlib.pyplot as plt

# define the function for plotting time series
def plot_time_series(data, sfreq, tmin=0, tmax=None):
    n_channels, n_samples = data.shape
    times = np.arange(n_samples) / sfreq
    if tmax is None:
        tmax = times[-1]
    mask = (times >= tmin) & (times <= tmax)
    
    fig, ax = plt.subplots()
    for i in range(n_channels):
        ax.plot(times[mask], data[i, mask], label=f'Channel {i+1}')
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Amplitude ($\mu V$)')
    plt.title('Time Series')
    ax.legend()
    plt.show()
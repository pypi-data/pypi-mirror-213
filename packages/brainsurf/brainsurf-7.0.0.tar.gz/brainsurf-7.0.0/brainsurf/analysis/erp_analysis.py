import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def erp_analysis(data, event_column, event_id, tmin=-0.2, tmax=0.8):
    """
    Perform ERP analysis on the given data.

    Parameters
    ----------
    data : pandas DataFrame
        EEG data with channels as columns and time as index.
    event_column : str
        Column name indicating the onset of each stimulus or trial.
    event_id : int or list of int
        Event ID(s) to use for epoching the data.
    tmin : float, optional
        Start time of the epoch in seconds relative to the event onset.
    tmax : float, optional
        End time of the epoch in seconds relative to the event onset.

    Returns
    -------
    erp : pandas DataFrame
        Average ERP waveform for each channel.
    """
    # Convert the event column to a list
    events = data[event_column].tolist()

    # Find the index of each event in the data
    event_index = [0]
    for i in range(1, len(events)):
        if events[i] != events[i-1]:
            event_index.append(i)

    # Create epochs from the data
    epoch_data = []
    for idx in event_index:
        epoch = data.iloc[idx + int(tmin*1000):idx + int(tmax*1000) + 1, :]
        epoch_data.append(epoch.values)
    epoch_data = np.array(epoch_data)

    # Compute the average of the epochs to obtain the ERP waveform
    erp = pd.DataFrame(epoch_data.mean(axis=0), columns=data.columns)

    # Visualize the ERP waveform
    plt.figure()
    plt.plot(erp.index, erp.values)
    plt.xlabel('Time (ms)')
    plt.ylabel('Amplitude (uV)')
    plt.title('ERP Waveform')
    plt.legend(erp.columns)

    # Extract ERP components of interest
    # ...

    return erp

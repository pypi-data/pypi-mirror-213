from mne.io import read_raw
from .eeg_data import EEGDataFactory

def convert_mff_to_eegdata(file_path):
    factory = EEGDataFactory()
    eeg_data = factory.create_eeg_data(file_path)
    return eeg_data

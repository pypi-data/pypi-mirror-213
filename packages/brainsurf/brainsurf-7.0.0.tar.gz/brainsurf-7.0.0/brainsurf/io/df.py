from .eeg_data import EEGDataFactory

def convert_df_to_eegdata(df):
    factory = EEGDataFactory()
    eegdata = factory.create_eeg_data(df)
    return eegdata

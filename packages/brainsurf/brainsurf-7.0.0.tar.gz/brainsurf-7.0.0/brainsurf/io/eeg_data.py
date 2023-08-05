import pandas as pd
import pyedflib
import mne
import numpy as np
from scipy.signal import welch
class EEGData:
    def __init__(self, **kwargs):
        self.data = pd.DataFrame(kwargs)

    def __len__(self):
        return len(self.data)
    def drop_columns(self, columns):
        """
        Drop specified columns from the EEGData object.

        Parameters:
            columns (str or list): The column(s) to drop.

        Returns:
            None
        """
        if isinstance(columns, str):
            columns = [columns]  # Convert single column name to a list

        existing_columns = list(self.data.columns)
        columns_to_drop = [col for col in columns if col in existing_columns]

        if columns_to_drop:
            self.data.drop(columns=columns_to_drop, inplace=True)
        else:
            print("Specified column(s) not found in the EEGData object.")
    def get_data(self):
        return self.data

    def data_length(self):
        length = 0
        for value in self.data.values():
            if isinstance(value, list):
                length = max(length, len(value))
            else:
                length = max(length, len(str(value)))
        return length

    def calculate_length(self, key=None):
        if key is None:
            # Calculate the length of all keys
            lengths = [len(str(value)) for value in self.data.values()]
            return max(lengths)
        else:
            # Calculate the length of a specific key
            if key in self.data:
                value = self.data[key]
                return len(str(value))
            else:
                raise KeyError(f"Key '{key}' does not exist in the EEGData object.")

    def keys(self):
        return self.data.keys()

    def set_data(self, **kwargs):
        for key, value in kwargs.items():
            if isinstance(value, pd.Series):
                value = value.to_frame()  # Convert Series to DataFrame
            self.data[key] = value
            
    def dropna(self):
        """
        Remove rows with missing values from the EEGData object.

        Returns:
            None
        """
        self.data.dropna(inplace=True)

    def summary(self, max_len=5):
        """
        Prints a summary of the EEGData object by displaying the first n_samples keys and their corresponding values.

        Parameters:
            n_samples (int): The number of key-value pairs to display. Default is 5.

        Returns:
            None
        """
        print(self.data.head(max_len))


    def add_data(self, key, value):
        self.data[key] = value

    def remove_data(self, key):
        del self.data[key]

    def __getitem__(self, key):
        return self.data[key]

    def get_values(self, key):
        """
        Get the values of a particular key from the EEGData object.

        Parameters:
            key (str): The key to retrieve the values for.

        Returns:
            The values associated with the key.
        """
        if key in self.keys():
            values = self.get_data()[key]
            return values
        else:
            raise KeyError(f"Key '{key}' does not exist in the EEGData object.")
        
    def extract_frequency_bands(self):
        if 'raw' in self.data and 'sec' in self.data:
            raw_data = self.data['raw']
            sec_data = self.data['sec']
            
            # Perform extraction of frequency bands from raw data if they don't exist
            if 'alpha' not in self.data:
                epoch_length = 1000  # Length of each epoch in milliseconds
                num_epochs = len(raw_data) // epoch_length
                pre_epochs = np.split(raw_data[:num_epochs * epoch_length], num_epochs)
                
                pre_features = []
                
                for epoch in pre_epochs:
                    f, psd = welch(epoch, fs=128)  # Adjust fs (sampling frequency) as per your data
                    
                    # Check if the frequency range contains data points
                    alpha_psd = psd[(f >= 8) & (f <= 13)]
                    alpha_power = np.mean(alpha_psd) if alpha_psd.any() else np.nan
                    pre_features.append(alpha_power)
                
                # Make sure the extracted features have the same length as the original data
                pre_features += [np.nan] * (len(raw_data) - len(pre_features))
                
                self.data['alpha'] = pre_features
                        
            if 'beta' not in self.data:
                pre_features = []
                
                for epoch in pre_epochs:
                    f, psd = welch(epoch, fs=128)  # Adjust fs (sampling frequency) as per your data
                    
                    # Check if the frequency range contains data points
                    beta_psd = psd[(f >= 13) & (f <= 30)]
                    beta_power = np.mean(beta_psd) if beta_psd.any() else np.nan
                    pre_features.append(beta_power)
                
                # Make sure the extracted features have the same length as the original data
                pre_features += [np.nan] * (len(raw_data) - len(pre_features))
                
                self.data['beta'] = pre_features
            
            if 'delta' not in self.data:
                pre_features = []
                
                for epoch in pre_epochs:
                    f, psd = welch(epoch, fs=128)  # Adjust fs (sampling frequency) as per your data
                    
                    # Check if the frequency range contains data points
                    delta_psd = psd[(f >= 1) & (f <= 4)]
                    delta_power = np.mean(delta_psd) if delta_psd.any() else np.nan
                    pre_features.append(delta_power)
                
                # Make sure the extracted features have the same length as the original data
                pre_features += [np.nan] * (len(raw_data) - len(pre_features))
                
                self.data['delta'] = pre_features
            
            if 'theta' not in self.data:
                pre_features = []
                
                for epoch in pre_epochs:
                    f, psd = welch(epoch, fs=128)  # Adjust fs (sampling frequency) as per your data
                    
                    # Check if the frequency range contains data points
                    theta_psd = psd[(f >= 4) & (f <= 8)]
                    theta_power = np.mean(theta_psd) if theta_psd.any() else np.nan
                    pre_features.append(theta_power)
                
                # Make sure the extracted features have the same length as the original data
                pre_features += [np.nan] * (len(raw_data) - len(pre_features))
                
                self.data['theta'] = pre_features

            if 'gamma' not in self.data:
                pre_features = []
                
                for epoch in pre_epochs:
                    f, psd = welch(epoch, fs=128)  # Adjust fs (sampling frequency) as per your data
                    
                    # Check if the frequency range contains data points
                    gamma_psd = psd[(f >= 30) & (f <= 50)]
                    gamma_power = np.mean(gamma_psd) if gamma_psd.any() else np.nan
                    pre_features.append(gamma_power)
                
                # Make sure the extracted features have the same length as the original data
                pre_features += [np.nan] * (len(raw_data) - len(pre_features))
                
                self.data['gamma'] = pre_features

            
            # Repeat the above code for other frequency bands (beta, theta, delta, gamma)
            # Adjust the frequency ranges and feature extraction accordingly
            
        else:
            raise ValueError("Required keys 'raw' and 'sec' are missing in the EEGData object.")
        
    def apply_ica(self, n_components=20, random_state=None):
        
        if 'raw' in self.data:
            raw_data = self.data['raw']
            
            # Convert raw data to MNE Raw object
            info = mne.create_info(ch_names=raw_data.columns.tolist(), sfreq=128)  # Adjust sfreq as per your data
            raw = mne.io.RawArray(raw_data.T.values, info)
            
            # Apply ICA
            ica = mne.preprocessing.ICA(n_components=n_components, random_state=random_state)
            ica.fit(raw)
            
            # Apply ICA to raw data
            ica_raw = ica.apply(raw)
            
            # Update raw data in EEGData object with cleaned data
            self.data['raw'] = pd.DataFrame(ica_raw.get_data().T, columns=raw_data.columns)
        else:
            raise ValueError("Required key 'raw' is missing in the EEGData object.")
        
    def apply_car(self):
        """
        Apply Common Average Reference (CAR) to the EEG data.

        Returns:
            None
        """
        if 'raw' in self.data:
            raw_data = self.data['raw']
            
            # Apply CAR
            car_data = raw_data - np.mean(raw_data, axis=1, keepdims=True)
            
            # Update raw data in EEGData object with CAR data
            self.data['raw'] = pd.DataFrame(car_data, columns=raw_data.columns)
        else:
            raise ValueError("Required key 'raw' is missing in the EEGData object.")




class EEGDataFactory:
    def create_eeg_data(self, input_file):
        if isinstance(input_file, pd.DataFrame):
            eeg_data = EEGData()
            for column in input_file.columns:
                eeg_data.add_data(column, input_file[column])
            return eeg_data
        #CSV
        elif input_file.endswith('.csv'):
            data = self.parse_csv(input_file)
            if 'sec' in data.columns and 'EEG' in data.columns and 'alpha' in data.columns and 'beta' in data.columns and 'delta' in data.columns and 'theta ' in data.columns:
                # CSV data with sec, alpha, beta,  delta and theta columns            
                return EEGData(sec=data['sec'], raw=data['EEG'], alpha=data['alpha'], beta=data['beta'], theta=data['theta '], delta =data['delta'])
            elif 'sec' in data.columns:
                # CSV data with raw and sec columns
                return EEGData(sec=data['sec'], raw=data['EEG'])
            else:
                # CSV data with only raw data
                return EEGData(raw=data['EEG'])
        #EDF
        elif input_file.endswith('.edf'):
            # Parse EDF data
            data = self.parse_edf(input_file)
            channel_names = data['channel_names']
            raw_data = data['raw_data']
            return EEGData(channel_names=channel_names, raw_data=raw_data)
    
        elif input_file.endswith('.mff'):
            raw = mne.io.read_raw_egi(input_file)
            eeg_data = raw.get_data()
            time_points = raw.times
            baseline = pd.DataFrame(data=eeg_data.T, columns=raw.ch_names)
            baseline['sec'] = time_points
            return baseline
            # Create EEGData object with the extracted data           
        
        elif input_file.endswith('.xlsx'):
            data = self.parse_xlsx(input_file)
            # Extract relevant information from the XLSX data
            if 'sec' in data.columns and 'EEG' in data.columns and 'alpha' in data.columns and 'beta' in data.columns and 'delta' in data.columns and 'theta ' in data.columns:
                    # CSV data with sec, alpha, beta, and gamma columns            
                    return EEGData(sec=data['sec'], raw=data['EEG'], alpha=data['alpha'], beta=data['beta'], theta=data['theta '], delta =data['delta'])
            elif 'sec' in data.columns:
                    # CSV data with raw and time columns
                    return EEGData(sec=data['sec'], raw=data['EEG'])
            else:
                    # CSV data with only raw data
                    return EEGData(raw=data['EEG'])
        else:
            raise ValueError("Invalid file format. Only CSV, EDF, MFF, and XLSX files are supported.")
    
    

    def parse_csv(self, input_file):
        data = pd.read_csv(input_file)
        return data

    def parse_edf(self, input_file):
        f = pyedflib.EdfReader(input_file)
        channel_names = f.getSignalLabels()
        raw_data = []
        for i in range(f.signals_in_file):
            raw_data.append(f.readSignal(i))
        f.close()
        data = {'channel_names': channel_names, 'raw_data': raw_data}
        return data
    
    def parse_xlsx(self, input_file):
        data = pd.read_excel(input_file)
        return data
    
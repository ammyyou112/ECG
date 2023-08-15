import numpy as np
import pandas as pd
import scipy
import os
from scipy.signal import find_peaks, medfilt


def preprocess_ecg_and_behavior(data_path, sampling_rate):
    # Load data_without_outliers.csv file
    # Path to the data folder containing the data_without_outliers.csv file
    data = r'C:\Users\Ammad\Desktop\ECG Signal Toolbox\data\data_without_outliers'
    data_file_path = os.path.join(data, 'data_without_outliers.csv')
    preprocessed_data = pd.read_csv(data_file_path)
    # preprocessed_data = data.copy()

    # Apply a bandpass filter to the ECG signal
    lowcut = 0.5
    highcut = 50.0
    nyquist = 0.5 * sampling_rate
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = scipy.signal.butter(4, [low, high], btype='band')
    preprocessed_data['filtered_ecg'] = scipy.signal.lfilter(b, a, preprocessed_data['ECG'])

    # Remove duplicate rows based on 'onset_ms' column
    preprocessed_data = preprocessed_data.drop_duplicates(subset='onset_ms', keep='first').reset_index(drop=True)

    # Normalize the filtered ECG signal
    preprocessed_data['normalized_ecg'] = (preprocessed_data['filtered_ecg'] - np.mean(preprocessed_data['filtered_ecg'])) / np.std(preprocessed_data['filtered_ecg'])

    # Preprocess 'difficulty' column
    preprocessed_data['difficulty'] = preprocessed_data['difficulty'].map({'easy': 0, 'hard': 1})

    # Preprocess 'correctResponse' column
    preprocessed_data['correctResponse'] = preprocessed_data['correctResponse'].map({'GORight': 0, 'GOLeft': 1, 'GOLleft': 2})

    # Preprocess 'participantResponse' column
    preprocessed_data['participantResponse'] = preprocessed_data['participantResponse'].map({'GORight': 0, 'GOLeft': 1, 'NoGo': 2})

    # Preprocess 'RT' column: Fill missing values with median
    preprocessed_data['RT'].fillna(preprocessed_data['RT'].median(), inplace=True)

    # Convert the ecg_signal to a numpy array
    ecg_signal = np.array(preprocessed_data['filtered_ecg'])

    # Perform peak detection on the entire ECG data
    peaks, _ = find_peaks(ecg_signal, height=0.5, distance=100)

    # Create an array of artifact indices based on the non-peak locations
    artifact_indices = np.setdiff1d(np.arange(len(ecg_signal)), peaks)

    # Apply median filter to remove artifacts
    window_size = 3  # Adjust the window size as needed
    preprocessed_data['filtered_ecg'] = medfilt(preprocessed_data['filtered_ecg'], kernel_size=window_size)

    return preprocessed_data

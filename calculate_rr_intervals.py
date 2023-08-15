import pandas as pd
import numpy as np

def calculate_rr_intervals_ecg(preprocess_data, sample_rate):
    try:
        """
        Calculate RR intervals from the 'onset_ms' column.

        Parameters:
            preprocess_data (pd.DataFrame): DataFrame containing preprocessed data.
            sampling_rate (float): The actual sampling rate of the ECG data.

        Returns:
            pd.DataFrame: DataFrame containing RR intervals in seconds with 'RR_intervals' column.
        """
        # Calculate the time differences between consecutive rows using 'onset_ms' column
        time_diff_ms = preprocess_data['onset_ms'].diff()
        time_diff_sec = time_diff_ms / 1000  # Convert to seconds

        # Convert the numpy array to a DataFrame
        rr_intervals_df = pd.DataFrame({'RR_intervals': time_diff_sec})

        # Drop the last row to match the length of preprocess_data DataFrame
        rr_intervals_df = rr_intervals_df[:-1]

        # Remove the first row with NaN in RR_intervals
        rr_intervals_df = rr_intervals_df.dropna(subset=['RR_intervals'], axis=0, how='any')

        # Convert 'RR_intervals' column to float data type
        rr_intervals_df['RR_intervals'] = rr_intervals_df['RR_intervals'].astype(float)

        return rr_intervals_df

    except Exception as e:
        print("An error occurred while calculating RR intervals:", str(e))
        return None

import os
import pandas as pd
import numpy as np
import scipy.signal

def calculate_heart_rate(rr_intervals_df, sampling_rate):
    try:
        """
        Calculate heart rate from RR intervals.

        Parameters:
            rr_intervals_df (pd.DataFrame): DataFrame containing RR intervals data.
            sampling_rate (float): The actual sampling rate of the ECG data.

        Returns:
            pd.DataFrame: DataFrame containing heart rate values with 'onset_ms' as index and 'Heart_Rate' column.
        """
        # Calculate heart rate from RR intervals
        heart_rate = 60 / rr_intervals_df['RR_intervals']

        # Create a DataFrame with 'onset_ms' as index and heart rate
        heart_rate_df = pd.DataFrame({'Heart_Rate': heart_rate}, index=rr_intervals_df.index)

        return heart_rate_df

    except Exception as e:
        print("An error occurred while calculating heart rate:", str(e))
        return None
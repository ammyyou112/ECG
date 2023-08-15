import pandas as pd
import numpy as np

def calculate_hrv(rr_intervals, window_size):
    try:
        rmssd_values = []
        sdnn_values = []
        hrv_values = []

        for i in range(len(rr_intervals) - window_size + 1):
            window_rr_intervals = rr_intervals[i:i+window_size]

            rr_diff = np.diff(window_rr_intervals)
            rr_diff_sq = [diff ** 2 for diff in rr_diff]
            mean_rr_diff_sq = np.mean(rr_diff_sq)
            rmssd = np.sqrt(mean_rr_diff_sq)
            rmssd_values.append(rmssd)

            sdnn = np.std(window_rr_intervals)
            sdnn_values.append(sdnn)

            hrv = rmssd / sdnn
            hrv_values.append(hrv)

        hrv_df = pd.DataFrame({'RMSSD': rmssd_values, 'SDNN': sdnn_values, 'HRV': hrv_values})
        return hrv_df

    except Exception as e:
        print("An error occurred while calculating HRV:", str(e))
        return None

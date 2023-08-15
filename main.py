import os
import pandas as pd
import plotly.express as px
import numpy as np
import scipy.signal
from preprocess_data import preprocess_ecg_and_behavior
from calculate_rr_intervals import calculate_rr_intervals_ecg
from cardiac_timing import calculate_heart_rate
from calculate_hrv import calculate_hrv
from visualize_data import visualize_ecg_signals, explore_hrv_behavioral_patterns
from analyze_behaviour import analyze_behavioral_patterns
from correlation_analysis import investigate_correlations
from statistical_analysis import perform_statistical_analysis
from interpret_results import interpret_results
from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__, static_url_path='/static')

# Initialize global variables for analysis results
ecg_plot_div = None
hrv_behavior_div = None
behavioral_analysis_div = None
correlation_heatmap_div = None
statistical_analysis_div = None
interpretation_div = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run_analysis', methods = ['POST'])

def run_analysis():
    global ecg_plot_div, hrv_behavior_div, behavioral_analysis_div, correlation_heatmap_div, statistical_analysis_div, interpretation_div
    try:
        #Get the sampling rate from submission
        sampling_rate = int(request.form['sampling_rate'])
        # Path to the data folder containing the data_without_outliers.csv file
        data_folder = r'C:\Users\Ammad\Desktop\ECG Signal Toolbox\data\data_without_outliers'
        data_file_path = os.path.join(data_folder, 'data_without_outliers.csv')

        sampling_rate = 500

        # Load the data without outliers
        # data_without_outliers = pd.read_csv(data_file_path)

        # Preprocess the ECG signal and behavior data
        preprocess_data = preprocess_ecg_and_behavior(data_file_path, sampling_rate)
        if preprocess_data is not None:
            print("Data preprocessing successful!")
        # Calculate RR intervals
        rr_intervals_df = calculate_rr_intervals_ecg(preprocess_data, sampling_rate)
        if rr_intervals_df is not None:
            print("RR intervals calculation successful!")
        # Merge rr_intervals_df with preprocessed_data based on index
        preprocess_data = pd.merge(preprocess_data, rr_intervals_df, left_index=True, right_index=True)
        # Drop rows with NaN values in the 'RR_intervals' column
        rr_intervals_df = rr_intervals_df.dropna(subset=['RR_intervals'], axis=0, how='any')

        # Convert 'RR_intervals' column to a NumPy array and then create a new DataFrame
        preprocess_data['RR_intervals'] = preprocess_data['RR_intervals'].astype(float)
        rr_intervals = preprocess_data['RR_intervals'].astype(float)
        # rr_intervals_df.to_csv('rr_intervals.csv', index=False)

        # Calculate heart rate DataFrame
        heart_rate_df = calculate_heart_rate(rr_intervals_df, sampling_rate)
        if heart_rate_df is not None:
            print("Heart rate calculation successful!")

        # Merge heart rate information back into the preprocessed data
        merged_df = pd.merge(preprocess_data, heart_rate_df, left_index=True, right_index=True)

        # Calculate RMSSD, SDNN, and HRV using rolling window approach
        hrv_df = calculate_hrv(rr_intervals, window_size=3)
        if hrv_df is not None:
            print("HRV calculation successful!")
        # Print the resulting HRV DataFrame
        print(hrv_df)
        merged_data_df = pd.merge(merged_df, hrv_df, left_index=True, right_index=True)
        print(merged_data_df)

        # Visualizations:
        # visualize ecg signals
        ecg_plot_div = visualize_ecg_signals(merged_data_df)

        # Explore HRV and behavioral patterns
        hrv_behavior_div = explore_hrv_behavioral_patterns(merged_data_df)

        # Visualize behavioral patterns
        behavioral_analysis_div = analyze_behavioral_patterns(merged_data_df)

        # Statistical Analysis
        # Investigate correlations between behavioral metrics and ECG features
        correlation_heatmap_div = investigate_correlations(merged_data_df)

        # Call the function with your DataFrame
        statistical_analysis_div = perform_statistical_analysis(merged_data_df)

        # Call the function
        interpretation_div = interpret_results(merged_data_df)

        return render_template('results.html',
                               ecg_plot_div=ecg_plot_div,
                               hrv_behavior_div=hrv_behavior_div,
                               behavioral_analysis_div=behavioral_analysis_div,
                               correlation_heatmap_div=correlation_heatmap_div,
                               statistical_analysis_div=statistical_analysis_div,
                               interpretation_div=interpretation_div)
    except Exception as e:
        error_message = "An Error Occured: " + str(e)
        return render_template('error.html', error_message=error_message)
        # print("An error occurred:", str(e))

@app.route('/get_analysis_result', methods=['GET'])
def get_analysis_result():
    try:
        # Assuming you have already computed the necessary analysis results in your main() function
        # You can adapt this code based on how you're storing and structuring your analysis results
        analysis_results = {
            "ecg_plot_div": ecg_plot_div,
            "hrv_behavior_div": hrv_behavior_div,
            "behavioral_analysis_div": behavioral_analysis_div,
            "correlation_heatmap_div": correlation_heatmap_div,
            "statistical_analysis_div": statistical_analysis_div,
            "interpretation_div": interpretation_div
        }
        return jsonify(analysis_results)
    except Exception as e:
        error_message = "An error occurred while retrieving analysis results: " + str(e)
        return jsonify({"error": error_message})

if __name__ == "__main__":
    app.run(debug=True)

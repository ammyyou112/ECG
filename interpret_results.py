import statsmodels.api as sm

def interpret_results(merged_data_df):
    try:
        # Summarize the correlation analysis
        print("Correlation Matrix:")
        correlation_matrix = merged_data_df[['HRV', 'RMSSD', 'SDNN', 'RT']].corr()
        print(correlation_matrix)
        print("\n")

        # Summarize the T-Tests or ANOVA
        print("T-Tests and ANOVA:")
        print("Summarize the results of the T-Tests and ANOVA that were previously performed.")
        print("\n")

        # Summarize the Linear Regression Analysis
        print("Linear Regression Analysis:")
        regression_model = sm.OLS(merged_data_df['RT'], sm.add_constant(merged_data_df[['HRV', 'RMSSD', 'SDNN']]))
        regression_results = regression_model.fit()
        print(regression_results.summary())
        print("\n")

        # Interpretation
        print("Interpretation:")
        print("The correlation matrix indicates the relationships between ECG features and RT.")
        print("T-Tests and ANOVA results provide insights into the significance of ECG features across different responses.")
        print("The linear regression analysis shows how ECG features predict RT.")
        print("Consider both statistical and practical significance when interpreting the results.")
        print("Further research could explore additional factors that contribute to the observed relationships.")
        print("\n")

    except Exception as e:
        print("An error occurred while interpreting results:", str(e))

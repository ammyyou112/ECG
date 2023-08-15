import scipy.stats as stats
import statsmodels.api as sm

def perform_statistical_analysis(merged_data_df):
    try:
        # Correlation Analysis
        correlation_matrix = merged_data_df[['HRV', 'RMSSD', 'SDNN', 'RT']].corr()
        print("Correlation Matrix:")
        print(correlation_matrix)
        print("\n")

        # T-Tests or ANOVA (depending on data distribution)
        print("T-Tests:")
        for response in merged_data_df['correctResponse'].unique():
            subset = merged_data_df[merged_data_df['correctResponse'] == response]
            for ecg_feature in ['HRV', 'RMSSD', 'SDNN']:
                t_statistic, p_value = stats.ttest_ind(subset[ecg_feature], merged_data_df[ecg_feature])
                print(f"T-Test for {ecg_feature} with Correct Response {response}:")
                print("T-Statistic:", t_statistic)
                print("P-Value:", p_value)
                print("\n")

        # Linear Regression Analysis using statsmodels
        X = merged_data_df[['HRV', 'RMSSD', 'SDNN']]
        X = sm.add_constant(X)  # Add constant term for intercept
        y = merged_data_df['RT']

        regression_model = sm.OLS(y, X).fit()

        print("Linear Regression Analysis using statsmodels:")
        print(regression_model.summary())
        print("\n")

    except Exception as e:
        print("An error occurred during statistical analysis:", str(e))
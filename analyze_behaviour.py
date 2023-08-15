import plotly.express as px

def analyze_behavioral_patterns(merged_data_df):
    try:
        # Analyze difficulty distribution
        difficulty_counts = merged_data_df['difficulty'].value_counts()
        print("Difficulty Distribution:")
        print(difficulty_counts)

        # Analyze correct vs. participant responses
        response_counts = merged_data_df.groupby(['correctResponse', 'participantResponse']).size().unstack()
        print("\nResponse Analysis:")
        print(response_counts)

        # Analyze response time distribution
        response_time_stats = merged_data_df['RT'].describe()
        print("\nResponse Time Statistics:")
        print(response_time_stats)

        # Analyze Behavioral Patterns Across Difficulty Levels
        fig1 = px.box(merged_data_df, x='difficulty', y='HRV', title="Behavioral Patterns Across Difficulty Levels - HRV")
        fig1.update_xaxes(title="Difficulty Level")
        fig1.update_yaxes(title="HRV")

        # Response Time vs. ECG Features
        fig2 = px.scatter(merged_data_df, x='RT', y='HRV', title="Response Time vs. HRV")
        fig2.update_xaxes(title="Response Time")
        fig2.update_yaxes(title="HRV")

        # Comparison of ECG Features and Behavioral Responses
        fig3 = px.box(merged_data_df, x='correctResponse', y='HRV', title="Comparison of HRV Across Behavioral Responses")
        fig3.update_xaxes(title="Correct Response")
        fig3.update_yaxes(title="HRV")

        fig4 = px.box(merged_data_df, x='correctResponse', y='RMSSD', title="Comparison of RMSSD Across Behavioral Responses")
        fig4.update_xaxes(title="Correct Response")
        fig4.update_yaxes(title="RMSSD")

        fig5 = px.box(merged_data_df, x='correctResponse', y='SDNN', title="Comparison of SDNN Across Behavioral Responses")
        fig5.update_xaxes(title="Correct Response")
        fig5.update_yaxes(title="SDNN")

        graph_div1 = fig1.to_html()
        graph_div2 = fig2.to_html()
        graph_div3 = fig3.to_html()
        graph_div4 = fig4.to_html()
        graph_div5 = fig5.to_html()

        return graph_div1, graph_div2, graph_div3, graph_div4, graph_div5

    except Exception as e:
        print("An error occurred during behavioral analysis:", str(e))

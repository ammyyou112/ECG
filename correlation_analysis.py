import plotly.express as px

def investigate_correlations(merged_data_df):
    try:
        # Select relevant columns for correlation analysis
        relevant_columns = ['difficulty', 'correctResponse', 'participantResponse', 'RT', 'HRV', 'RMSSD', 'SDNN']

        # Calculate correlation matrix
        correlation_matrix = merged_data_df[relevant_columns].corr()

        # Print correlation matrix
        print("\nCorrelation Matrix:")
        print(correlation_matrix)

        # Create a heatmap using Plotly Express
        fig = px.imshow(correlation_matrix, color_continuous_scale='viridis', zmin=-1, zmax=1)
        fig.update_layout(
            title='Correlation Heatmap: Behavioral Data vs ECG Features',
            xaxis=dict(title="Features"),
            yaxis=dict(title="Features")
        )

        # Convert the figure to HTML format
        graph_div = fig.to_html()

        return graph_div

    except Exception as e:
        print("An error occurred while investigating correlations:", str(e))

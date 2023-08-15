import plotly.graph_objects as go


def visualize_ecg_signals(merged_data_df):
    try:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=merged_data_df.index, y=merged_data_df['ECG'], mode='lines', name='Raw ECG'))
        fig.add_trace(
            go.Scatter(x=merged_data_df.index, y=merged_data_df['filtered_ecg'], mode='lines', name='Filtered ECG'))
        fig.add_trace(
            go.Scatter(x=merged_data_df.index, y=merged_data_df['normalized_ecg'], mode='lines', name='Normalized ECG'))

        fig.update_layout(
            title=f"ECG Signal Variation for Trial {merged_data_df['trial'].values[0]}",
            xaxis_title="Sample",
            yaxis_title="Amplitude",
            legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
            autosize=False,
            width=800,
            height=400,
        )

        graph_div = fig.to_html()
        return graph_div
    except Exception as e:
        print("An error occurred during ECG signal visualization:", str(e))


def visualize_correlation_heatmap(merged_data_df):
    try:
        behavioral_columns = ['difficulty', 'correctResponse', 'participantResponse', 'RT']
        ecg_feature_columns = ['HRV', 'RMSSD', 'SDNN']

        # Decode the encoded values for better understanding
        merged_data_df['decoded_difficulty'] = merged_data_df['difficulty'].map({0: 'Easy', 1: 'Hard'})
        merged_data_df['decoded_correctResponse'] = merged_data_df['correctResponse'].map({0: 'GORight', 1: 'GOLeft', 2: 'GOLleft'})
        merged_data_df['decoded_participantResponse'] = merged_data_df['participantResponse'].map({0: 'GORight', 1: 'GOLeft', 2: 'NoGo'})

        correlation_matrix = merged_data_df[behavioral_columns + ecg_feature_columns].corr()

        fig = go.Figure(data=go.Heatmap(
            z=correlation_matrix.values,
            x=correlation_matrix.columns,
            y=correlation_matrix.index,
            colorscale='RdBu_r',
            zmin=-1,
            zmax=1
        ))

        fig.update_layout(
            title='Correlation Heatmap: Behavioral Data vs ECG Features',
            xaxis_title="Features",
            yaxis_title="Features",
            xaxis_nticks=len(correlation_matrix.columns),
            yaxis_nticks=len(correlation_matrix.index),
        )

        graph_div = fig.to_html()
        return graph_div
    except Exception as e:
        print("An error occurred during correlation heatmap visualization:", str(e))


def explore_hrv_behavioral_patterns(merged_data_df):
    try:
        if 'RT' in merged_data_df.columns and 'HRV' in merged_data_df.columns:
            fig = go.Figure()

            for difficulty_level in merged_data_df['difficulty'].unique():
                filtered_data = merged_data_df[merged_data_df['difficulty'] == difficulty_level]
                scatter = go.Scatter(
                    x=filtered_data['RT'],
                    y=filtered_data['HRV'],
                    mode='markers',
                    name=f'Difficulty {difficulty_level}',
                    text=filtered_data['trial'],
                    marker=dict(
                        size=10,
                        opacity=0.7,
                        line=dict(width=2)
                    )
                )
                fig.add_trace(scatter)

            fig.update_layout(
                title='Scatter Plot of HRV vs RT by Difficulty Level',
                xaxis_title='Response Time (RT)',
                yaxis_title='HRV',
                legend_title='Difficulty'
            )

            graph_div = fig.to_html()
            return graph_div
        else:
            print("Required columns 'RT' and/or 'HRV' not found in the DataFrame.")
            print("Available columns:", merged_data_df.columns)
    except Exception as e:
        print("An error occurred during HRV and behavioral patterns exploration:", str(e))
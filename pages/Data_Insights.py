import pandas as pd
import streamlit as st
import plotly.graph_objects as go

    
# Bar Chart: Distribution of Overall Feelings
def plot_overall_feelings(df):
    counts = df['Overall'].value_counts()
    fig = go.Figure(go.Bar(x=counts.index, y=counts.values))
    fig.update_layout(
        title='Distribution of Overall Feelings',
        xaxis_title='Overall Feeling',
        yaxis_title='Count',
        xaxis={'categoryorder':'total descending'}
    )
    return fig


# Box Plot: Distribution of Sentiment Scores
def plot_sentiment_score_distribution(df):
    fig = go.Figure(go.Box(y=df['Sentiment Score'], boxpoints='all', jitter=0.5, whiskerwidth=0.2))
    fig.update_layout(
        title='Distribution of Sentiment Scores',
        yaxis_title='Sentiment Score'
    )
    return fig


# Sentiment across different months
def generate_graph(df):
    monthly_sentiment = df.groupby('Month')['Sentiment Score'].mean().reset_index()
    sentiment_counts = df.groupby(['Month', 'Overall']).size().reset_index(name='Count')

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=monthly_sentiment['Month'], y=monthly_sentiment['Sentiment Score'], mode='lines+markers', name='Average Sentiment Score'))

    for label in sentiment_counts['Overall'].unique():
        df_filtered = sentiment_counts[sentiment_counts['Overall'] == label]
        fig.add_trace(go.Scatter(x=df_filtered['Month'], y=df_filtered['Count'], mode='lines+markers', name=label))
    fig.update_layout(
        title='Overall Sentiment Across Months',
        xaxis_title='Month',
        yaxis_title='Count / Average Score',
        legend_title='Legend'
    )
    return fig


def main():
    st.title("Business Data Insights")

    csv_file = st.file_uploader("Please upload Your Updated Business' Reviews", type=["csv"])

    if csv_file is None:
        st.warning("Please upload an updated CSV file.")
        return
    try:
        df = pd.read_csv(csv_file, parse_dates=['Date'], date_format='%Y-%m-%d')
    except (ValueError, KeyError):
        st.error("Error: Invalid date format in the CSV file. Please ensure the date format is 'YYYY-MM-DD'.")
        return

    st.title('Review Insights')
    st.sidebar.title('Filter Graph Options')

    selected_insights = st.sidebar.multiselect('Select Insights', ['Overall Sentiment Across Months',
                                                                    'Distribution of Overall Feelings',
                                                                    'Distribution of Sentiment Scores',
                                                                    ])

    if 'Distribution of Overall Feelings' in selected_insights:
        st.subheader('Distribution of Overall Feelings')
        fig1 = plot_overall_feelings(df)
        st.plotly_chart(fig1)

    if 'Overall Sentiment Across Months' in selected_insights:
        st.subheader('Overall Sentiment Across Months')
        fig2 = generate_graph(df)
        st.plotly_chart(fig2)

    if 'Distribution of Sentiment Scores' in selected_insights:
        st.subheader('Distribution of Sentiment Scores')
        fig3 = plot_sentiment_score_distribution(df)
        st.plotly_chart(fig3)

if __name__ == '__main__':
    main()
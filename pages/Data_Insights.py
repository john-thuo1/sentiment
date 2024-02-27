import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# Function to generate Line Graph: Trend of Sentiment Scores over Time
def plot_sentiment_scores(df):
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df['Date'], df['Sentiment Score'])
    ax.set_xlabel('Date')
    ax.set_ylabel('Sentiment Score')
    ax.set_title('Trend of Sentiment Scores over Time')
    ax.tick_params(axis='x', rotation=45)
    return fig

# Function to generate Bar Chart: Distribution of Overall Feelings
def plot_overall_feelings(df):
    fig, ax = plt.subplots(figsize=(8, 5))
    df['Overall'].value_counts().plot(kind='bar', ax=ax)
    ax.set_xlabel('Overall Feeling')
    ax.set_ylabel('Count')
    ax.set_title('Distribution of Overall Feelings')
    return fig

# Function to generate Box Plot: Distribution of Sentiment Scores
def plot_sentiment_score_distribution(df):
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.boxplot(df['Sentiment Score'])
    ax.set_ylabel('Sentiment Score')
    ax.set_title('Distribution of Sentiment Scores')
    return fig

# Function to show Sentiment across the different months
def generate_graph(df):
    monthly_sentiment = df.groupby('Month')['Sentiment Score'].mean()

    sentiment_counts = df.groupby(['Month', 'Overall']).size().unstack(fill_value=0)

    num_labels = len(sentiment_counts.columns)
    labels = sentiment_counts.columns

    # Plot the graph
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(monthly_sentiment.index, monthly_sentiment.values, label='Average Sentiment Score')

    if num_labels == 1 or num_labels == 2:
        ax.plot(sentiment_counts.index, sentiment_counts[labels[0]], label=labels[0])
    else:
        for label in labels:
            ax.plot(sentiment_counts.index, sentiment_counts[label], label=label)

    ax.set_xlabel('Month')
    ax.set_ylabel('Count / Average Score')
    ax.set_title('Overall Sentiment Across Months')
    ax.legend()

    return fig

# Function to generate Bar Chart: Monthly Count of Reviews
def plot_monthly_review_counts(df):
    fig, ax = plt.subplots(figsize=(10, 5))
    monthly_counts = df['Month'].value_counts().sort_index()
    monthly_counts.plot(kind='bar', ax=ax)
    ax.set_xlabel('Month')
    ax.set_ylabel('Count')
    ax.set_title('Monthly Count of Reviews')
    return fig

def main():
    st.title("Business Data Insights")

    csv_file = st.file_uploader("Please upload Your Updated Business' Reviews", type=["csv"])

    if csv_file is None:
        st.warning("Please upload an updated CSV file.")
        return

    try:
        df = pd.read_csv(csv_file)
        df['Date'] = pd.to_datetime(df['Date'])
        df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')
        df['Date'] = pd.to_datetime(df['Date'])
    except (ValueError, KeyError):
        st.error("Error: Invalid date format in the CSV file. Please ensure the date format is 'YYYY-MM-DD'.")
        return

    st.title('Review Insights')

    st.sidebar.title('Filter Options')

    # Display the graphs based on user selection
    selected_insights = st.sidebar.multiselect('Select Insights', ['Overall Sentiment Across Months', 'Trend of Sentiment Scores',
                                                                    'Distribution of Overall Feelings',
                                                                    'Distribution of Sentiment Scores',
                                                                    'Monthly Count of Reviews'])

    if 'Trend of Sentiment Scores' in selected_insights:
        st.subheader('Trend of Sentiment Scores over Time')
        fig = plot_sentiment_scores(df)
        st.pyplot(fig)

    if 'Distribution of Overall Feelings' in selected_insights:
        st.subheader('Distribution of Overall Feelings')
        fig = plot_overall_feelings(df)
        st.pyplot(fig)

    if 'Overall Sentiment Across Months' in selected_insights:
        st.subheader('Overall Sentiment Across Months')
        fig = generate_graph(df)
        st.pyplot(fig)

    if 'Distribution of Sentiment Scores' in selected_insights:
        st.subheader('Distribution of Sentiment Scores')
        fig = plot_sentiment_score_distribution(df)
        st.pyplot(fig)

    if 'Monthly Count of Reviews' in selected_insights:
        st.subheader('Monthly Count of Reviews')
        fig = plot_monthly_review_counts(df)
        st.pyplot(fig)

if __name__ == '__main__':
    st.set_option('deprecation.showPyplotGlobalUse', False)
    main()
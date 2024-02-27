import streamlit as st
import pandas as pd
import datetime

from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

# Load the NLP Model from Hugging Face
@st.cache_data
def load_model():
    tokenizer = AutoTokenizer.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')
    model = AutoModelForSequenceClassification.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')
    return tokenizer, model

# Sentiment Scoring
def sentiment_score(review, tokenizer, model):
    tokens = tokenizer.encode(review, return_tensors='pt')
    result = model(tokens)
    return int(torch.argmax(result.logits) + 1)


def main():
    st.title("Multilingual Sentiment Analysis Tool For Your Business")
    csv_file = st.file_uploader("Please upload Your Business' Reviews", type=["csv"])

    if csv_file is not None:
        df = pd.read_csv(csv_file)
        df['Sentiment Score'] = 0  
        snapshot = df.head(3)
        st.dataframe(snapshot) 

        # Load the model
        tokenizer, model = load_model()

        if st.button("Analyze"):
            df['Sentiment Score'] = df['Review'].apply(lambda x: sentiment_score(x[:512], tokenizer, model) if pd.notna(x) else 0)

            sentiment_mapping = {5: 'Positive', 4: 'Positive', 3: 'Neutral', 1: 'Negative', 2: 'Negative'}
            df['Overall'] = df['Sentiment Score'].map(sentiment_mapping)

            # Display the updated DataFrame
            st.dataframe(df.head())

            csv_file_name = datetime.datetime.now().strftime("%d-%m-%y") + '_updated_reviews.csv'
            csv = df.to_csv(index=False)

            st.download_button(
                label='Download CSV File',
                data=csv,
                file_name=csv_file_name,
                mime='text/csv'
            )


if __name__ == '__main__':
    main()
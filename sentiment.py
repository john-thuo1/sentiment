import streamlit as st
import pandas as pd
import datetime
import chardet
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch


# Load Model Tokenizers from hf
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


# Check the Structure of the Uploaded CSV
def check_csv_structure(df):
    required_columns = ['product_name', 'review', 'month', 'year']  # Convert to lowercase
    # Check if all required columns are present in the DataFrame
    missing_columns = [col for col in required_columns if col not in df.columns]

    return len(missing_columns) == 0, missing_columns


# Detect CSV File Encoding 
def read_encoding(csv_file):
    rawdata = csv_file.read()  
    detected_encoding = chardet.detect(rawdata)['encoding']
    csv_file.seek(0)

    # Read CSV using detected encoding ( utf8, latin1, iso-8859-1)
    df = pd.read_csv(csv_file, encoding=detected_encoding)

    # Convert column names to lowercase
    df.columns = df.columns.str.lower()

    return df


st.image("https://t4.ftcdn.net/jpg/05/07/99/33/360_F_507993376_rCbxKj9u6mXi7ei9CZiZFhWj0QpGnxOu.jpg", use_column_width=True)
def main():
    st.title("Opinion Mining Tool For Your Business")
    csv_file = st.file_uploader("Please upload Your Business' Reviews. Ensure that your CSV file contains the following columns: Product_Name, Review, Month, Year, and that they are named exactly as specified.", type=["csv"])


    if csv_file is not None:
        
        df = read_encoding(csv_file)
        
        structure_ok, missing_columns = check_csv_structure(df)
        
        if not structure_ok:
            st.error(f"The uploaded CSV file is missing required columns: {', '.join(missing_columns)}")
            return
        
        # Check for required Date Format in the CSV file 
        if not df['date'].str.match(r'\d{4}-\d{2}-\d{2}').all():
            df['date'] = pd.to_datetime(df['date'], format='%d-%m-%y')

        if "sentiment score" not in df.columns:
            df['sentiment score'] = 0  # Convert to lowercase
        else:
            df['sentiment score'] = 0  # Convert to lowercase
                     
        snapshot = df.head(5)
        st.dataframe(snapshot) 

        tokenizer, model = load_model()

        if st.button("Analyze"):
            df['sentiment score'] = df['review'].apply(lambda x: sentiment_score(x[:512], tokenizer, model) if pd.notna(x) else 0)

            sentiment_mapping = {5: 'Positive', 4: 'Positive', 3: 'Neutral', 1: 'Negative', 2: 'Negative'}
            df['overall'] = df['sentiment score'].map(sentiment_mapping)  # Convert to lowercase

            # Display the updated DataFrame
            st.dataframe(df.head())
            
            original_filename = csv_file.name.split('.')[0]
            csv_file_name = f"{original_filename}_updated_{datetime.datetime.now().strftime('%d-%m-%y')}.csv"
            csv = df.to_csv(index=False)

            st.download_button(
                label='Download CSV File',
                data=csv,
                file_name=csv_file_name,
                mime='text/csv'
            )


if __name__ == '__main__':
    main()

import streamlit as st
import pandas as pd
from openai import OpenAI
from decouple import config

client = OpenAI(
    api_key=config("OPENAI_API_KEY"),
)


def truncate_text(text, max_length):
    if len(text) > max_length:
        return text[:max_length] + "..."
    return text


def generate_initial_recommendation(business_data):
    message = ""
    for _, row in business_data.iterrows():
        review = row['Review']
        sentiment_score = row['Sentiment Score']
        review = truncate_text(review, 500)
        message += f"Review: {review}\nSentiment Score: {sentiment_score}\n"
    message = truncate_text(message, 4096)
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Provide a thorough Business Recommendation based on the reviews and sentiment scores."},
            {"role": "user", "content": message},
        ],
    )
    return response.choices[0].message.content.strip()


def generate_follow_up_response(chat_history):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=chat_history,
    )
    return response.choices[0].message.content.strip()


def main():
    st.title("Business Recommendation Chat")
    st.markdown(
        """
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
        """,
        unsafe_allow_html=True,
    )

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    file = st.file_uploader("Upload a CSV file for analysis", type=["csv"])
    
    if file is not None:
        business_data = pd.read_csv(file)
        st.subheader("Uploaded Business Data")
        st.dataframe(business_data)

        required_columns = ["Product_Name", "Review", "Sentiment Score"]
        if set(required_columns).issubset(business_data.columns):
            if 'initial_recommendation_done' not in st.session_state:
                recommendation = generate_initial_recommendation(business_data)
                st.session_state.chat_history.append({"role": "assistant", "content": recommendation})
                st.session_state.initial_recommendation_done = True


            for chat_message in st.session_state.chat_history:
                if chat_message["role"] == "user":
                    st.markdown(f"<i class='fa-solid fa-user'></i> <strong>{chat_message['content']}</strong>", unsafe_allow_html=True)
                else:  # role == "assistant"
                    st.markdown(f"<i class='fas fa-robot'></i> {chat_message['content']}", unsafe_allow_html=True)


            prompt = st.chat_input("Follow Up Question? Inquire from here ...")
            if prompt:
                st.session_state.chat_history.append({"role": "user", "content": prompt})
                follow_up_response = generate_follow_up_response(st.session_state.chat_history)
                st.session_state.chat_history.append({"role": "assistant", "content": follow_up_response})
                st.rerun()
        else:
            st.error("Error: The uploaded CSV file does not contain all the required columns.")

if __name__ == "__main__":
    main()

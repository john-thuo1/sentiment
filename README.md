### Video Recording and Deployment

1. [G1 Video Recording](https://drive.google.com/file/d/1YThAEbFXEbe7DsXZdseynq2p1KzIgwD5/view?usp=sharing)
2. [Hosted App Link](https://sentiment-g1.streamlit.app/)

### Project Setup Instructions

- Create a Virtual Environment using either Venv/ Conda
- Activate the Environment and  run ```pip install -r requirements.txt```

1. **PyTorch Library Installation:**
   - If PyTorch Installation fails via `requirements.txt`, please visit the [Official PyTorch Page](https://pytorch.org/) and follow the installation instructions. It is recommended to install PyTorch without CUDA support.

2. **Setting Up Secrets for Local Run:**
   - Create a `secrets.toml` file in the `./streamlit` directory within your project root folder. 
   
   - The structure of the `secrets.toml` file should be as follows:

     ```toml
     [openai]
     api_key = "Your API KEY"
     ```

     Replace `"Your API KEY"` with your actual OpenAI API Key. This file will be used to store sensitive information securely within your project.


3. **System Error Handling:**

   - The system verifies if the uploaded file conforms to the required file structure, notifying businesses about any missing columns.
   - Automatically detecting file encodings, the system ensures that files are read based on these encodings.
   - Date columns are converted to the required date format by the system.
   - To prevent key errors caused by columns specified in different formats, the system standardizes all columns to lowercase.

     ```
     streamlit run sentiment.py
     ```
     
### Project Testing

  - Download Flipkart Reviews Data in the `Dataset` Folder.
  - Upload the Dataset to the sentiment Page to generate the Sentiment Scores and Overall Sentiments for each of the Customer Reviews.
  - Download the Updated Reviews( e.g `Flipkart_updated_reviews_2019_11_01.csv`) and store them Locally.
  - Upload the Updated Reviews to Business Recommendations Page to get actionable recommendations from `gpt3.5-turbo` model and ask follow-up questions.
  - Upload the Updated Reviews to Data Insights to generate Insights such as Product Vs Sentiment, Distribution of sentiments across the year etc.

     


### Project Setup Instructions

1. **PyTorch Library Installation:**
   - To install the PyTorch library, please visit the [Official PyTorch Page](https://pytorch.org/) and follow the installation instructions. It is recommended to install PyTorch without CUDA support.

2. **Setting Up Secrets for Local Run:**
   - Create a `secrets.toml` file in the `./streamlit` directory within your project root folder. 
   
   - The structure of the `secrets.toml` file should be as follows:

     ```toml
     [openai]
     api_key = "Your API KEY"
     ```

     Replace `"Your API KEY"` with your actual OpenAI API Key. This file will be used to store sensitive information securely within your project.

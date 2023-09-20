from pathlib import Path
import streamlit as st
import openai
from PyPDF2 import PdfFileReader
from docx import Document
from transformers import pipeline
import torch
# from pymongo import MongoClient  # Commented out MongoDB import

# MongoDB URI from Streamlit secrets
# mongo_uri = st.secrets["MONGO_URI"]  # Commented out MongoDB URI

# Connect to MongoDB (do not include the database name in the URI)
# mongo_client = MongoClient(mongo_uri)  # Commented out MongoDB connection

# Specify the database and collection after connecting
# database_name = "streamlit-openai-nodejs-app"  # Commented out database name
# collection_name = "streamlit"  # Commented out collection name
# db = mongo_client[database_name]  # Commented out database connection
# collection = db[collection_name]  # Commented out collection connection

# Retrieve the OpenAI API key from Streamlit's secrets
openai_api_key = st.secrets["OPENAI_API_KEY"]

# Streamlit setup
st.title('OpenAI Chat')

# Load OpenAI API key
try:
    openai.api_key = openai_api_key
except KeyError:
    st.sidebar.write("You haven't set up your OpenAI API key yet.")

# Print the PyTorch version to the console
st.write(f'PyTorch version: {torch.__version__}')

# Set up the QA pipeline with a specific model and tokenizer
qa_pipeline = pipeline("question-answering", model="distilbert-base-cased-distilled-squad", tokenizer="distilbert-base-cased-distilled-squad")

# ... (rest of your code remains the same)

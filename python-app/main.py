from pathlib import Path
import streamlit as st
import openai
from PyPDF2 import PdfFileReader
from docx import Document
from transformers import pipeline
import torch
from pymongo import MongoClient
import os

# Retrieve the OpenAI API key from Streamlit's secrets
openai_api_key = st.secrets["OPENAI_API_KEY"]

# Retrieve MongoDB credentials from Streamlit's secrets
mongo_uri = st.secrets["MONGO_URI"]
mongo_user = st.secrets["MONGO_USER"]
mongo_pass = st.secrets["MONGO_PASS"]

# Streamlit setup
st.title('OpenAI Chat')

# Load OpenAI API key
try:
    openai.api_key = openai_api_key
except KeyError:
    st.sidebar.write("You haven't set up your OpenAI API key yet.")

# Function to connect to MongoDB
def connect_to_mongodb():
    # Build the MongoDB URI with credentials
    mongo_uri_with_auth = f"mongodb+srv://{mongo_user}:{mongo_pass}@{mongo_uri}/?retryWrites=true&w=majority"

    # Connect to MongoDB
    mongo_client = MongoClient(mongo_uri_with_auth)
    return mongo_client

# Connect to MongoDB
mongo_client = connect_to_mongodb()

# Database and collection setup
database_name = "streamlit-openai-nodejs-app"  # Replace with your database name
collection_name = "streamlit"  # Replace with your collection name

db = mongo_client[database_name]
collection = db[collection_name]

# Rest of your code...

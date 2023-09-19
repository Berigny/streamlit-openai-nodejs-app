from pathlib import Path
import streamlit as st
import openai
from PyPDF2 import PdfFileReader
from docx import Document
from transformers import pipeline
import torch
from pymongo import MongoClient
import os

# Streamlit setup
st.title('OpenAI Chat')

# Load OpenAI API key from environment variables
try:
    openai.api_key = os.environ['OPENAI_API_KEY']
except KeyError:
    st.sidebar.write("You haven't set up your API key yet.")

# Function to connect to MongoDB
def connect_to_mongodb():
    mongo_uri = st.secrets["MONGO_URI"]
    mongo_client = MongoClient(mongo_uri)
    return mongo_client

# Connect to MongoDB
mongo_client = connect_to_mongodb()

# Database and collection setup
database_name = "streamlit-openai-nodejs-app"  # Replace with your database name
collection_name = "streamlit"  # Replace with your collection name

db = mongo_client[database_name]
collection = db[collection_name]

# Print the PyTorch version to the console
st.write(f'PyTorch version: {torch.__version__}')

# Set up the QA pipeline with a specific model and tokenizer
qa_pipeline = pipeline("question-answering", model="distilbert-base-cased-distilled-squad", tokenizer="distilbert-base-cased-distilled-squad")

# File upload logic...
uploaded_file = st.file_uploader("Choose a file", type=['txt', 'pdf', 'docx'])

if uploaded_file:
    file_extension = Path(uploaded_file.name).suffix

    # Read the contents based on file type
    try:
        if file_extension == '.txt':
            file_contents = uploaded_file.read().decode("utf-8")
        elif file_extension == '.pdf':
            pdf_reader = PdfFileReader(uploaded_file)
            file_contents = ''
            for page in range(pdf_reader.getNumPages()):
                file_contents += pdf_reader.getPage(page).extract_text()
        elif file_extension == '.docx':
            doc = Document(uploaded_file)
            file_contents = ' '.join([p.text for p in doc.paragraphs])
        else:
            st.error("Unsupported file type")
            file_contents = ''
    except Exception as e:
        st.error(f"Could not read file: {e}")
        file_contents = ''
else:
    file_contents = ''

# Define a maximum allowed number of tokens. Adjust as necessary.
MAX_TOKENS = 4000  # Adjust this value based on the model's maximum token limit and your specific requirements

def get_openai_response(message):
    # Check the number of tokens in the message
    if len(message.split()) > MAX_TOKENS:
        return f"Input is too long. Maximum allowed tokens is {MAX_TOKENS}."

    # Get a response from the OpenAI API
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": message},
        ]
    )
    message_content = response['choices'][0]['message']['content']
    return message_content

# Input field for user to input their query or chat
user_input = st.text_input("You: ", file_contents)

if user_input:
    if len(file_contents) > 0:
        try:
            answer = qa_pipeline(question=user_input, context=file_contents, max_length=512, truncation=True)
            st.write(f'Answer: {answer["answer"]}')
        except Exception as e:
            st.write(f'An error occurred: {str(e)}')
    else:
        # If no file is uploaded, use the OpenAI API to respond to the chat message
        st.write(f'Assistant: {get_openai_response(user_input)}')

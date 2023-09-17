from pathlib import Path
import streamlit as st
import openai
import os
from PyPDF2 import PdfFileReader
from docx import Document
from transformers import pipeline, AutoTokenizer
import torch

# Print the PyTorch version to the console
print(torch.__version__)

# Set up the QA pipeline with a specific model and tokenizer
qa_pipeline = pipeline("question-answering", model="distilbert-base-cased-distilled-squad", tokenizer="distilbert-base-cased-distilled-squad")

# Load the pre-trained tokenizer
tokenizer = AutoTokenizer.from_pretrained("gpt2")

# A simple dataset (for illustration purposes)
dataset = [
    "Hello world!", 
    "OpenAI develops artificial general intelligence.", 
    "Python is a popular programming language."
]

# Adding a text input for users to submit data for fine-tuning
user_submission = st.text_input("Submit data for fine-tuning:")

if user_submission:
    dataset.append(user_submission)
    # Fine-tune the tokenizer with the new submission
    tokenizer.add_tokens(user_submission.split())
    st.write("Thank you for your submission!")

# Set up OpenAI API key
try:
    openai.api_key = os.environ['OPENAI_API_KEY']
except KeyError:
    st.sidebar.write("""
    You haven't set up your API key yet.
    """)
    exit(1)
    
st.title('OpenAI Chat')

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
    # Here we change tokenizer.tokenize to tokenizer.encode
    # because AutoTokenizer does not have a tokenize method
    tokens = tokenizer.encode(message)
    token_count = len(tokens)

    if token_count > MAX_TOKENS:
        return f"Input is too long ({token_count} tokens). Maximum allowed tokens is {MAX_TOKENS}."
    
    # your existing get_openai_response code
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": message},
        ]
    )
    message_content = response['choices'][0]['message']['content']
    return message_content

user_input = st.text_input("You: ", file_contents)

if user_input:
    if file_contents:
        # If a file is uploaded, try to answer the question based on the file's content
        answer = qa_pipeline(question=user_input, context=file_contents, max_length=512, truncation="only_second")
        st.write(f'Answer: {answer["answer"]}')
    else:
        # If no file is uploaded, use the OpenAI API to respond to the chat message
        st.write(f'Assistant: {get_openai_response(user_input)}')

# Get a question from the user
user_question = st.text_input("Ask a question about the document:")

if user_question and file_contents:
    # Get an answer to the question based on the content of the uploaded file
    answer = qa_pipeline(question=user_question, context=file_contents, truncation=True)
    
    # Display the answer
    st.write(f'Answer: {answer["answer"]}')

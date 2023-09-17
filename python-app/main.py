from pathlib import Path
import streamlit as st
import openai
import os
from PyPDF2 import PdfFileReader
from docx import Document

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

user_input = st.text_input("You: ", file_contents)

# Function to communicate with OpenAI API
def get_openai_response(message):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": message},
        ]
    )
    message_content = response['choices'][0]['message']['content']
    return message_content
    
if user_input:
    st.write(f'Assistant: {get_openai_response(user_input)}')

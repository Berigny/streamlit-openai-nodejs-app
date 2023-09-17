import streamlit as st
import openai
import os

# Set up OpenAI API key
try:
    openai.api_key = os.environ['OPENAI_API_KEY']
except KeyError:
    st.sidebar.write("""
    You haven't set up your API key yet.
    """)
    exit(1)
    
st.title('OpenAI Chat')
user_input = st.text_input("You: ", "")

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

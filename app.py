import os
import base64
import streamlit as st
from dotenv import load_dotenv

from openai import OpenAI


# Load environment variables from .env file
load_dotenv()

def decode_api_key(encoded_api_key):
    decoded_bytes = base64.b64decode(encoded_api_key.encode('utf-8'))
    decoded_str = str(decoded_bytes, 'utf-8')
    return decoded_str

# Load and decode the OpenAI API key from environment variables
encoded_api_key = os.getenv("OPENAI_API_KEY")
openai_api_key=""
if encoded_api_key:
    openai_api_key = decode_api_key(encoded_api_key)
else:
    st.error("OpenAI API key not found in environment variables")
    st.stop()
client = OpenAI(
    # This is the default and can be omitted
    api_key=openai_api_key,
)


st.title("💬 My Chatbot")
st.caption("🚀 A Streamlit chatbot powered by Me")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

def prompt_generator(history):
    prompt=f"""
            You are an intelligent bot to answer the user question with history of conversation 
            question with history of conversation :{history}
            """
    return prompt

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    try:
        print("before model training!!")
        print(f"api key : {openai_api_key}")
        print(f"meesages : {str(st.session_state.messages)}")
        print(prompt_generator(st.session_state.messages))
        print("after prompt")
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt_generator(st.session_state.messages),
                }
            ],
            model="gpt-3.5-turbo",
        )
        print("response")
        msg = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": msg})
        st.chat_message("assistant").write(msg)
    except Exception as e:
        st.error(f"An error occurred: {e}")
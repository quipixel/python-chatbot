#%%writefile app.py

import streamlit as st
import google.generativeai as genai
#import dotenv
#import os

#dotenv.load_dotenv()

api_key=st.getenv("API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

def get_response(messages):
    try:
      response = model.generate_content(messages)
      return response
    except Exception as e:
      return f"Error {str(e)}"

def fetch_conversation_history():
    if 'messages' not in st.session_state:
        st.session_state['messages'] = [
            {"role": "user", "parts": "System Prompt: You are TeachGemini - the world's leading expert on study techniques. Answer any questions about study techniques and structure your responses in ther form of a short, but detailed study plan. Answer any question in 100 words or less. "}
        ]
    return st.session_state['messages']


st.title("TeachGemini - My Virtual Study Assistant")

user_input = st.chat_input("You: ")


if user_input:
    messages = fetch_conversation_history()
    messages.append({"role": "user", "parts": user_input})
    response = get_response(messages)
    messages.append({"role": "model", "parts": response.candidates[0].content.parts[0].text})

    for message in messages:
        if message["role"] == "model":
            st.write(f"TeachGemini: {message['parts']}")
        elif message["role"] == "user" and ("System Prompt" not in message["parts"]) :
            st.write(f"You: {message['parts']}")
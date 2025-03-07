import openai
import streamlit as st
from constants import GPT_API_KEY, GPT_MODEL

def openai_send_message(messages, temperatura=0, stream=False):
    openai.api_key = st.session_state[GPT_API_KEY]
    model = st.session_state[GPT_MODEL]
    return openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperatura,
        stream=stream
    )

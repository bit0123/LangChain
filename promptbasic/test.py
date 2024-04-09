import streamlit as st
from model import ask_openai

st.title("LangChain::StreamLit Test App.")

prompt = st.text_input("Enter your Prompt:")
submit = st.button("Submit")

if submit:
    st.text("")
    response = ask_openai(prompt)
    st.text(response)

import requests
import streamlit as st
from model import ask_openai

st.title("LangChain::StreamLit Test App.")

question = st.text_input("Enter your Question:")
submit = st.button("Submit")

if submit:
    st.text("")
    response = ask_openai(question)
    st.text(response)

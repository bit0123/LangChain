import requests
import streamlit as st

st.title("LangChain::FastAPI::StreamLit Test App.")

prompt = st.text_input("Enter your Prompt:")
submit = st.button("Submit")

if submit:
    st.text("")
    response = requests.get("http://localhost:8000/ask_openai", params={"prompt":prompt})
    if response.status_code == 200:
        st.text(response.json())


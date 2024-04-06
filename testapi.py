import requests
import streamlit as st

st.title("LangChain::FastAPI::StreamLit Test App.")

question = st.text_input("Enter your Question:")
submit = st.button("Submit")

if submit:
    st.text("")
    response = requests.get("http://localhost:8000/ask_openai", params={"question":question})
    if response.status_code == 200:
        st.text(response.json())


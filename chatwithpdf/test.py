import streamlit as st
from dotenv import load_dotenv
from model import ChatBot

chatbot = ChatBot()

st.title("Chat with Pdf using LangChain::Streamlit::FAIIS")

st.header("Select Pdf to Upload")
file = st.file_uploader("Upload File", type="pdf")

if file is not None:
    chatbot.init_chain()
    chatbot.process_pdf_file(file)

    query = st.text_input("Write your Query:")

    if st.button("Ask") and query is not None:

        response = chatbot.ask_query(query)
        
        st.write(response)

        chatbot.update_qa_history(query, response)
        qa_history = chatbot.get_qa_history()

        with st.sidebar:
            st.header("QA History")
            # with st.expander("Expand History"):
            for qa in qa_history:
                st.info("Human: "+qa[0])
                st.info("AI: "+qa[1])




    
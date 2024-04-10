import os
import pickle
from pypdf import PdfReader
from dotenv import load_dotenv

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores.faiss import FAISS

from langchain.llms.openai import OpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.chains import RetrievalQAWithSourcesChain, ConversationChain, ConversationalRetrievalChain
from langchain.memory import ConversationBufferWindowMemory, ConversationBufferMemory, ReadOnlySharedMemory
from langchain.prompts import PromptTemplate



class ChatBot:
 
    qa_history = []

    def __init__(self) -> None:
        load_dotenv()

    def init_chain(self):
        llm = OpenAI(model="gpt-3.5-turbo-instruct", temperature=0)
        self.chain = load_qa_chain(llm, chain_type="stuff")


    def process_pdf_file(self, file:str):

        file_name = file.name[:-4]

        reader = PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()

        text_chunks = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200).split_text(text)

        if os.path.exists(f"{file_name}.pkl"):
            with open(f"{file_name}.pkl", "rb") as f:
                self.chunks_embeddings = pickle.load(f)
            print("Embedding Loaded from the disk.")
        else:
            embedding = OpenAIEmbeddings()
            self.chunks_embeddings = FAISS.from_texts(text_chunks, embedding=embedding)
            with open(f"{file_name}.pkl", "wb") as f:
                pickle.dump(self.chunks_embeddings, f)
        
            print("Embedding Stored in the disk.")


    def ask_query(self, query:str):
        similar_chunks = self.chunks_embeddings.similarity_search(query=query)
        # qa_chain = ConversationalRetrievalChain.from_llm(llm, retriever=chunks_embeddings.as_retriever(), get_chat_history=lambda h : h, condense_question_prompt=prompt, memory = memory)
        
        response = self.chain.run(input_documents=similar_chunks, question=query, return_answer_only=True)
        # response = qa_chain({"question":query}, return_answer_only=True)

        return response


    def get_qa_history(self):
        return self.qa_history


    def update_qa_history(self, q:str, a:str):
        self.qa_history.append((q,a))


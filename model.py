import os
from dotenv import load_dotenv
from langchain.llms import OpenAI

load_dotenv()

llm = OpenAI(model="gpt-3.5-turbo-instruct", temperature=.9)


def ask_openai(question:str):
    response = llm(question)
    return response

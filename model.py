import os
from dotenv import load_dotenv
from langchain.llms import OpenAI

load_dotenv()

llm = OpenAI(temperature=.9)


def ask_openai(question:str):
    response = llm(question)
    return response

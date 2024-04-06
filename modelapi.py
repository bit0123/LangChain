import os
from dotenv import load_dotenv
from langchain.llms import OpenAI
from fastapi import FastAPI

load_dotenv()

api = FastAPI()
llm = OpenAI(temperature=.9)

@api.get('/ask_openai')
async def ask_openai(question:str):
    response = llm(question)
    return response

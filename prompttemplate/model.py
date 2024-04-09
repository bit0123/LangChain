from dotenv import load_dotenv
from langchain.llms import OpenAI
from langchain.chains import LLMChain, SimpleSequentialChain, SequentialChain
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory, ConversationBufferWindowMemory


load_dotenv()

# Prompt Template for Tourist Attraction in a given Country
attractions_template = PromptTemplate(
    input_variables=["country_name"],
    template="Suggest top 3 tourist attractions in {country_name} following the rules: [Attraction Number]. [Attraction Name], [Location] : [Brief Description of Attraction] Example: 1. Cox Bazar, Chittagong : Largest Sea Beach across the world. Famous for sea food and beach."
)

# Prompt Template for Nearby Hotels given Tourist Attractions
hotel_template = PromptTemplate(
    input_variables=["attractions"],
    template="For each of the bellow mentioned 3 tourist attractions, suggest top 3 nearby hotels seperated by new line following the rules: [Hotel Number]. [Hotel Name], [Hotel Location]. Example: 1. Cox Bazar, Chittagong: \n 1. Hotel A, Chittagong \n 2. Hotel B, Chittagong \n 3. Hotel C, Chittagong \n\n  Bellow are the tourist attractions: {attractions}"
)

# Memory to store Conversation history
# memory = ConversationBufferMemory(input_key='country_name', memory_key='tourist_attraction')
memory = ConversationBufferWindowMemory(input_key="country_name", memory_key="tourist_attraction", human_prefix="\nHuman", ai_prefix="\nAI", k=4)

# LLM
llm = OpenAI(model="gpt-3.5-turbo-instruct", temperature=.9)
attraction_chain = LLMChain(llm=llm, prompt=attractions_template, output_key="attractions", memory=memory, verbose=True)
hotel_chain = LLMChain(llm=llm, prompt=hotel_template, output_key="hotels", memory=memory, verbose=True)
seq_chain = SequentialChain(chains=[attraction_chain, hotel_chain], input_variables=["country_name"], output_variables=["attractions", "hotels"], verbose=True)


# Interface to interact bwtween LLM and User's prompt
def get_response(prompt:str):
    response = seq_chain(prompt)
    return response["attractions"], response["hotels"], memory.buffer

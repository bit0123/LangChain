import re
import streamlit as st
from model import get_response

# Define a regular expression pattern to match ordered list items
pattern = r'\d+\.\s*(.*?)(?=\n\d+\.\s*|\Z)'  # Matches digits followed by a dot and optional space, then captures the text


st.title("Chat Application using Langchain::Streamlit")

# prompt = st.text_input("Enter your Prompt:") # Example: Suggest me top 5 tourist spots in Bangladesh
st.header("Enter the country name you want to visit")
prompt = st.text_input("Country Name:") # Example: Bangladesh

sidebar = st.sidebar

def on_select_destination():
    st.sidebar.text(st.session_state["destination"])


if st.button("Submit"):

    tabs_options = []
    tabs_descriptions = []
    tabs_hotels = []

    response_attractions, response_hotels, memory_buffer = get_response(prompt=prompt)

    # Use re.findall to extract all matches of the pattern in the text
    items_attraction = re.findall(pattern, response_attractions, re.DOTALL)
    # Strip each item to remove leading/trailing whitespaces
    response_attractions_splits = [item.strip() for item in items_attraction]

    # Use re.findall to extract all matches of the pattern in the text
    items_hotels = re.findall(pattern, response_hotels, re.DOTALL)
    # Strip each item to remove leading/trailing whitespaces
    response_hotelss_splits = [item.strip() for item in items_hotels]

    
    flag = False
    N = len(response_attractions_splits)
    H = len(response_hotelss_splits)
    H_per_N = H//N
    for i in range(N):
        tabs_hotels.append(response_hotelss_splits[i*H_per_N:i*H_per_N+H_per_N])

    print(len(response_attractions_splits), len(response_attractions_splits))
    for option in response_attractions_splits: 
        if len(option)>2: 
            option_split = option.split(":")

            tabs_options.append(option_split[0])
            tabs_descriptions.append(option_split[1])

    tabs = st.tabs([option.split(",")[0] for option in tabs_options])
    for i in range(len(tabs_options)):
        tabs[i].header(tabs_options[i])
        tabs[i].text(tabs_descriptions[i])
        if i < len(tabs_hotels):
            tabs[i].text("Recommended Hotels:")
            hotels = tabs_hotels[i]
            print(hotels)
            for hotel in hotels[-3:]:
                tabs[i].text(hotel)

    with st.sidebar:
        st.header("Chat History")
        with st.expander("Expand History"):
            st.info(memory_buffer)



css = '''
<style>

	# .stTabs [data-baseweb="tab-list"] {
	# 	gap: 3px;
    # }

	.stTabs [data-baseweb="tabs"] {
        height: 50px;
        white-space: pre-wrap;
		background-color: teal;
		border-radius: 4px 4px 0px 0px;
		gap: 1px;
		padding-top: 10px;
		padding-bottom: 10px;
    }

	# .stTabs [aria-selected="true"] {
  	# 	background-color: red;
	# }

</style>
'''

st.markdown(css, unsafe_allow_html=True)

    



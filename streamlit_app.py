import streamlit as st
import anthropic

# Set your API key directly here
ANTHROPIC_API_KEY = st.secrets["key"]

# Sidebar for links
with st.sidebar:
    st.title("🤖 ChatBot Enhanced Technical Support")
    st.markdown("ChatBot Enhanced Technical Support is a chatbot application designed to provide technical support and answer questions related to the National Institute of Transport (NIT).")
   
# Title for the Streamlit app
st.title("🤖 ChatBot Enhanced Technical Support")

# Read NIT information from the text file
try:
    with open("nit_info.txt", "r") as file:
        nit_context = file.read()
except FileNotFoundError:
    st.error("NIT information file not found. Please make sure 'nit_info.txt' is present.")
    st.stop()

# Input for new questions
question = st.text_input(
    "💬 Ask something about NIT",
    placeholder="What courses does NIT offer?",
)

# Process the question if API key is provided
if question:
    prompt = f"""{anthropic.HUMAN_PROMPT} Here's some information about NIT:\n\n
    {nit_context}\n\n\n\n{question}{anthropic.AI_PROMPT}"""

    client = anthropic.Client(api_key=ANTHROPIC_API_KEY)
    response = client.completions.create(
        prompt=prompt,
        stop_sequences=[anthropic.HUMAN_PROMPT],
        model="claude-v1",  # Use "claude-2" for Claude 2 model if available
        max_tokens_to_sample=100,
    )
    
    # Display the response
    st.write("### Answer")
    st.write(response.completion)

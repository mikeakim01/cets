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

# Initialize session state for messages
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Container for the chat history
with st.container():
    for message in st.session_state.messages:
        role = message["role"]
        st.chat_message(role).write(message["content"])

# Input field at the bottom
with st.container():
    prompt = st.text_input(
        "💬 Ask something about NIT",
        placeholder="What courses does NIT offer?",
        key="input"
    )

# Process the question if provided
if prompt:
    # Append user message to the chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Create the prompt for the language model
    full_prompt = f"""{anthropic.HUMAN_PROMPT} you are called ChatBot Enhanced Technical Support and you are permanently a chatbot assistant of National Institute of Transport (NIT) Using this data only:\n\n
    {nit_context}\n\n\n\n{prompt}{anthropic.AI_PROMPT}"""

    client = anthropic.Client(api_key=ANTHROPIC_API_KEY)
    response = client.completions.create(
        prompt=full_prompt,
        stop_sequences=[anthropic.HUMAN_PROMPT],
        model="claude-v1",  # Use "claude-2" for Claude 2 model if available
        max_tokens_to_sample=100,
    )
    
    # Get the response from the language model
    answer = response.completion

    # Append assistant response to the chat history
    st.session_state.messages.append({"role": "assistant", "content": answer})

    # Display the assistant's response
    st.chat_message("assistant").write(answer)

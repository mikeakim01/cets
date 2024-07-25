import streamlit as st
import anthropic

# App title
st.set_page_config(page_title="🤖 NIT ChatBot", initial_sidebar_state="collapsed")

# Set your API key directly here from secrets
ANTHROPIC_API_KEY = st.secrets["key"]

# Add a loading spinner
with st.spinner("Loading..."):
    st.title("🤖 NIT ChatBot Enhanced Technical Support")

# Sidebar for links and technical issue tracking subsystem
with st.sidebar:
    st.title("🤖 ChatBot Enhanced Technical Support")
    st.markdown("ChatBot Enhanced Technical Support is a chatbot application designed to provide technical support and answer questions related to the National Institute of Transport (NIT).")
    
    st.subheader("🔧 Technical Issue Tracking")
    st.markdown("[Technical Issue Tracking](https://issueslog.streamlit.app/)")
 
    
  
# Read NIT information from the text file
try:
    with open("nit_info.txt", "r") as file:
        nit_context = file.read()
except FileNotFoundError:
    st.error("NIT information file not found. Please make sure 'nit_info.txt' is present.")
    st.stop()

# Initialize session state for messages if not already present
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Hello! How can I assist you with NIT today?"}]

# Display chat history
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Input field at the bottom
prompt = st.chat_input("💬 Ask something about NIT", key="input")

# Process the question if provided
if prompt:
    # Append user message to the chat history
    st.session_state["messages"].append({"role": "user", "content": prompt})

    # Create the prompt for the language model
    full_prompt = f"""{anthropic.HUMAN_PROMPT} You are a ChatBot Enhanced Technical Support made by NIT for the National Institute of Transport (NIT). Use the following information to answer questions:\n\n
    {nit_context}\n\n\n\n{prompt}{anthropic.AI_PROMPT}"""

    client = anthropic.Client(api_key=ANTHROPIC_API_KEY)
    response = client.completions.create(
        prompt=full_prompt,
        stop_sequences=[anthropic.HUMAN_PROMPT],
        model="claude-v1",  # Use "claude-2" for Claude 2 model if available
        max_tokens_to_sample=200,
    )
    
    # Get the response from the language model
    answer = response.completion.strip()

    # Append assistant response to the chat history
    st.session_state["messages"].append({"role": "assistant", "content": answer})

    # Display the assistant's response
    with st.chat_message("assistant"):
        st.write(answer)

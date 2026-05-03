import streamlit as st
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load environment variables from .env file
load_dotenv()

# Initialize API client
# Make sure to set GEMINI_API_KEY in your .env file
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key) if api_key and api_key != "your_gemini_api_key_here" else None

# Set page config for aesthetics
st.set_page_config(page_title="AI Custom Assistant", page_icon="🤖", layout="centered")

# Custom CSS for better UI
st.markdown("""
<style>
    .stChatMessage {
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

st.title("🤖 Custom AI Assistant")

# Sidebar for settings
with st.sidebar:
    st.header("⚙️ Settings")
    system_prompt_choice = st.selectbox(
        "Select Persona:",
        ["General Assistant", "Coding Assistant", "Tutor", "Friend", "Sarcastic Bot"]
    )
    
    # Map choice to actual system prompt instructions
    personas = {
        "General Assistant": "You are a helpful and friendly AI assistant. Answer queries concisely and accurately.",
        "Coding Assistant": "You are an expert software engineer. Provide clean, efficient, and well-documented code. Explain concepts clearly and concisely.",
        "Tutor": "You are a patient and knowledgeable tutor. Do not give direct answers immediately; instead, guide the user to find the answer through hints and questions.",
        "Friend": "You are a supportive, casual, and empathetic friend. Use conversational language, emojis, and be very relatable.",
        "Sarcastic Bot": "You are a highly sarcastic and cynical AI. You still help the user, but not before making a snarky or passive-aggressive comment about their request."
    }
    
    system_prompt = personas[system_prompt_choice]
    
    st.markdown("---")
    st.markdown("**About this app:**")
    st.markdown("This chatbot uses Streamlit and the Gemini API to maintain a real-time conversational history with different personas.")
    
    st.markdown("---")
    if st.button("🗑️ Reset Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# Warning if API key is not set
if not client:
    st.warning("⚠️ Please set your `GEMINI_API_KEY` in the `.env` file to use this chatbot.")
    st.info("You can get a free API key from [Google AI Studio](https://aistudio.google.com/).")

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Type your message here..."):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    if client:
        # Prepare conversation history for the API
        contents = []
        for msg in st.session_state.messages:
            # Gemini roles are 'user' and 'model'
            role = "user" if msg["role"] == "user" else "model"
            contents.append(types.Content(role=role, parts=[types.Part.from_text(text=msg["content"])]))
            
        config = types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=0.7,
        )

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            
            try:
                # Call the Gemini API with streaming
                with st.spinner("Thinking..."):
                    response_stream = client.models.generate_content_stream(
                        model='gemini-2.5-flash',
                        contents=contents,
                        config=config
                    )
                
                full_response = ""
                for chunk in response_stream:
                    if chunk.text:
                        full_response += chunk.text
                        message_placeholder.markdown(full_response + "▌")
                
                message_placeholder.markdown(full_response)
                
                # Add assistant response to chat history
                st.session_state.messages.append({"role": "assistant", "content": full_response})
                
            except Exception as e:
                st.error(f"An API error occurred: {str(e)}")

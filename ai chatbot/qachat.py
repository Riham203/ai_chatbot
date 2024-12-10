from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai

# Load environment variables from the .env file
load_dotenv()

# Configure the API key for the Gemini model
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

# Function to get a response from Gemini
def get_gemini_response(question, history):
    prompt = f"""You are an AI assistant. Here's the conversation so far:\n\n
    {''.join([f'{role}: {text}' for role, text in history])}\n\n
Now, here's the user's new query: {question}\n\n
Please provide a comprehensive and informative response."""
    
    try:
        # Send the message to the model and get the response
        response = chat.send_message(prompt, stream=False)
        
        # Check if response has candidates
        if response and response.candidates:
            # Extract and concatenate the text from each part
            response_parts = response.candidates[0].content.parts
            response_text = "\n".join(part.text for part in response_parts)
            return response_text
        else:
            return "No response generated. Please try again."
    except Exception as e:
        return f"An error occurred: {e}"

# Set up Streamlit app configuration
st.set_page_config(page_title="Chatbot Demo")
st.header("Gemini LLM Chatbot Application")

# Initialize chat history in Streamlit's session state
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# Text input and submit button
input = st.text_input("Input: ", key="input")
submit = st.button("Ask the question")

if submit and input:
    # Get response from Gemini model
    response = get_gemini_response(input, st.session_state['chat_history'])
    st.session_state['chat_history'].append(("You", input))
    
    # Append the response from the chatbot to the chat history
    st.session_state['chat_history'].append(("Bot", response))

# Display the chat history
st.subheader("The chat history")
for role, text in st.session_state['chat_history']:
    st.write(f"{role}: {text}")
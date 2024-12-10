from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai

# Load environment variables from the .env file
load_dotenv()

# Configure the API key for Gemini Pro
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Load the Gemini Pro model
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

# Function to get a response from Gemini based on Beck's Cognitive Theory
def get_gemini_response(question, history):
    prompt = f"""You are an AI expert psychologist who knows Beck's Cognitive Theory very well. 
    There are 3 important parameters in Beck's Cognitive Theory to understand the Depression, 
    1. Cognitive Triad 2. Negative Self Schema 3. Faulty Information Processing. 
    You need to act like a conversational AI agent who is psychologist to ask questions to 
    the user to identify the cognitve triad mechanisms in user.
    
    You need to think logically as below:
    1. You need to consider previous historic conversation provided.
    2. You need to ask questions to get the views about the cognitive triad parameters in user; 
    cognitve triad parameters include i. negativity towards self ii. negativity towards future 
    iii. negativity towards world (friends, family, colleagues, relatives, teachers etc.) 
    Ask the questions indirectly, do not explicitly say about you are asking information about 
    cognitive triad.
    3. Strictly ask questions about the parameters one at a time. Do not ask at once about all 
    the cognitive triad parameters at once, it should be like counselling.
    Ask about only one cognitive triad parameter at once. Do not ask too much in one question. 
    4. You are concentrating on only cognitve triad parameters, not on negative self schema 
    and faulty information processing.
    5. Your first message in the conversation is already provided to the user like "Hello, 
    Greetings of the day.". 
    Strictly do not wish again like "hello", "hi", etc. Come to the point directly.
    6. To get the information of the user about cognitive triad mechanisms, ask the relevant 
    information from the user wherever required. So if user's first message is Greetings, 
    then do not reply with the greeting again, you can start fetching information about 
    cognitive triad.
    7. Your question should be crisp. Question should not be lengthy.
    
    Here's the conversation so far: \n\n 
    {''.join([f'{role}: {text} ' for role, text in history])} \n\n 
    Now, here's the user's new query: {question} \n\n 
    Please provide a comprehensive and informative response."""
    
    response = chat.send_message(prompt, stream=False)
    return response

# Initialize Streamlit app configuration
st.set_page_config(page_title="Psychological Support Chatbot")

# Set header for the app
st.header("Cognitive Triad Chatbot")

# Initialize session state for chat history if not present
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = [("Bot", "Hello, Greetings of the day.")]

# Input field for user query and a submit button
input = st.text_input("Input: ", key="input")
submit = st.button("Ask the question")

# Handle user input
if submit and input:
    # Get response from Gemini based on user input and chat history
    response = get_gemini_response(input, st.session_state['chat_history'])
    
    # Add user input to chat history
    st.session_state['chat_history'].append(("User", input))
    
    # Extract response text from Gemini's response structure
    response_filter = response.candidates[0].content.parts
    response_text = ' '.join(part.text for part in response_filter)
    
    # Add the chatbot's response to chat history
    st.session_state['chat_history'].append(("Bot", response_text))

# Display the chat history
st.subheader("The Chat History")
for role, text in st.session_state['chat_history']:
    st.write(f"{role}: {text}")
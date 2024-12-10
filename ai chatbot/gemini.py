from google.generativeai import generativeai as genai
import os

# Configure the API key for genai
GOOGLE_API_KEY = "AIzaSyDNszyIFgkB5vu_-Z8-DlcLWgdPlKIQppo"
genai.configure(api_key=GOOGLE_API_KEY)

# Define the model only once
model = genai.GenerativeModel("gemini-1.5-flash")

# Function to get Gemini response
def get_gemini_response(input_text):
    try:
        # Generate the response
        response = model.generate_text(input_text)

        # Check if candidates are available
        if response and response.candidates:
            # Extract and return the text from the first candidate
            response_text = response.candidates[0].text
            return response_text
        else:
            return "No response generated from the model."
    except AttributeError as e:
        return f"An error occurred: {e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"
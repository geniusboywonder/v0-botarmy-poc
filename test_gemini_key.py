
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv() # Load environment variables from .env file

# Load the API key from environment variables
api_key = os.getenv("GOOGLE_GENAI_API_KEY")

if not api_key:
    print("Error: GOOGLE_GENAI_API_KEY not found in environment variables.")
    print("Please set it in your .env file or directly in your environment.")
else:
    try:
        genai.configure(api_key=api_key)
        print("Listing available Gemini models:")
        for m in genai.list_models():
            if "generateContent" in m.supported_generation_methods:
                print(f"- {m.name}")
        print("\nAttempting to use models/gemini-1.5-pro-latest model:")
        model = genai.GenerativeModel('gemini-1.5-pro-latest')
        response = model.generate_content("Hello, Gemini!")
        print("Gemini API key is valid and models/gemini-1.5-pro-latest model is accessible! Response:", response.text)
    except Exception as e:
        print(f"Error: Gemini API key might be invalid or there's a connection issue. Details: {e}")

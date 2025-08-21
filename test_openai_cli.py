import os
import sys
from pathlib import Path
import openai
from dotenv import load_dotenv

# Add project root to Python path to allow imports if needed in future
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_openai_connection():
    """
    Tests the connection to the OpenAI API using the key from the .env file.
    """
    print("--- OpenAI Connection Test ---")

    # 1. Load environment variables from .env file
    print("1. Loading environment variables from .env file...")
    load_dotenv()

    # 2. Get API Key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("\n❌ ERROR: OPENAI_API_KEY not found in .env file.")
        print("   Please make sure your .env file exists and contains the key.")
        return

    if api_key == "your_openai_api_key_here":
        print("\n❌ ERROR: You are using the placeholder API key.")
        print("   Please replace 'your_openai_api_key_here' in the .env file with your actual key.")
        return

    print(f"2. Found API key ending in '...{api_key[-4:]}'")

    # 3. Test API Call
    print("3. Attempting to connect to OpenAI API...")
    try:
        client = openai.OpenAI(api_key=api_key)

        test_response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hello!"}],
            max_tokens=5,
            temperature=0.1
        )

        response_content = test_response.choices[0].message.content
        print("4. Received response from OpenAI.")

        print("\n✅ SUCCESS: OpenAI API connection is working correctly!")
        print(f"   Model: gpt-3.5-turbo")
        print(f"   Response: '{response_content.strip()}'")

    except openai.AuthenticationError:
        print("\n❌ ERROR: Authentication failed. Your API key is likely invalid or disabled.")
    except openai.NotFoundError:
        print("\n❌ ERROR: The model 'gpt-3.5-turbo' was not found. This may indicate an issue with your account or OpenAI's service.")
    except openai.RateLimitError:
        print("\n❌ ERROR: You have exceeded your OpenAI API rate limit or quota.")
        print("   Please check your OpenAI account usage and billing details.")
    except Exception as e:
        print(f"\n❌ An unexpected error occurred: {e}")

if __name__ == "__main__":
    test_openai_connection()

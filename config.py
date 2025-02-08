import os
from dotenv import load_dotenv

# Load environment variables
dotenv_loaded = load_dotenv()

# Debugging: Check if .env is actually loading
if not dotenv_loaded:
    print("⚠️  Error: .env file NOT loaded!")
    exit()

EMAIL = os.getenv("EMAIL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Debugging: Check if variables exist
if not EMAIL:
    print("⚠️  Error: EMAIL is missing from .env")
if not OPENAI_API_KEY:
    print("⚠️  Error: OPENAI_API_KEY is missing from .env")

# Print output
print("Email:", EMAIL if EMAIL else "[NOT FOUND]")
print("OpenAI Key:", "[HIDDEN]" if OPENAI_API_KEY else "[NOT FOUND]")

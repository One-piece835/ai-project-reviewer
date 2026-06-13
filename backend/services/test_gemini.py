# test_gemini.py

import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

print("Starting...")

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)

print("Sending request...")

response = model.generate_content(
    "Say hello in one sentence."
)

print(response.text)
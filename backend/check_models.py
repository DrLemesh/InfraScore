
import os
import google.generativeai as genai

api_key = os.environ.get('GEMINI_API_KEY')
if not api_key:
    print("No API Key found")
    exit(1)

print(f"Using API Key: {api_key[:5]}...")
genai.configure(api_key=api_key)

try:
    print("Listing available models...")
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"- {m.name}")
except Exception as e:
    print(f"Error listing models: {e}")

import os
from google import genai
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

MODEL = "gemini-3.5-flash"

def ask_gemini_with_file(file_path, prompt):
    uploaded_file = client.files.upload(file=file_path)
    response = client.models.generate_content(
        model=MODEL,
        contents=[uploaded_file, prompt]
    )
    return response.text

def ask_gemini_text(prompt):
    response = client.models.generate_content(
        model=MODEL,
        contents=prompt
    )
    return response.text
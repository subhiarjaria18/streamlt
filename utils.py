import os
import requests
import fitz  # PyMuPDF
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def extract_text_from_pdf(uploaded_file) -> str:
    """
    Extracts text content from a PDF file-like object.
    """
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text.strip()


def generate_questions(text: str, num: int) -> list:
    """
    Sends a prompt to Groq API using llama-3.1-8b-instant to generate relevant questions.
    """
    api_url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {os.getenv('GROQ_API_KEY')}",
        "Content-Type": "application/json"
    }

    prompt = f"""You are an expert educational assistant. 
Based on the content below, generate {num} unique, relevant, and conceptual questions that test understanding. 
Do not include answers. Avoid repetition and make them clear and educational. 

Content:
{text[:4000]}
"""

    data = {
        "model": "llama-3.1-8b-instant",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 1000
    }

    res = requests.post(api_url, headers=headers, json=data)

    if res.status_code == 200:
        reply = res.json()['choices'][0]['message']['content']
        return [q.strip("- ").strip() for q in reply.strip().split("\n") if q.strip()]
    else:
        return [f"Error: {res.status_code} - {res.text}"]

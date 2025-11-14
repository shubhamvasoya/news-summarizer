import os
import requests
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

def summarize_text(text, summary_type):
    if summary_type.startswith("Layman"):
        style_prompt = (
            "Rewrite the following news article in very simple English that a 10-year-old "
            "can understand. Use short sentences, simple vocabulary, and clear explanations.\n\n"
        )
    else:
        style_prompt = (
            "Rewrite the news article in technical and professional language. Include relevant "
            "economic, scientific, policy, or geopolitical terminology and provide a structured, "
            "concise, expert-level summary.\n\n"
        )

    payload = {
        "model": "meta-llama/llama-3.1-70b-instruct:free",
        "messages": [
            {"role": "user", "content": style_prompt + text}
        ]
    }

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            json=payload,
            headers=headers
        )
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]

    except Exception as e:
        print("Summarization error:", e)
        return "Summary generation failed!"

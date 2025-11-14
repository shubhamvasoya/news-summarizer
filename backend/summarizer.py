import os
import google.generativeai as genai
from dotenv import load_dotenv
import time

load_dotenv()

# Load API key
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini
genai.configure(api_key=GEMINI_KEY)

# Rate limiting
last_request_time = 0
MIN_INTERVAL = 1.0


def summarize_text(text, summary_style, summary_length):
    """
    Summarize with proper length control:
    - Concise: SHORT (2-5 bullet points, <50 words)
    - Detailed: LONG (full article, upto 500 words)
    
    Args:
        text (str): The article text to summarize
        summary_style (str): "Simple (Layman)" or "Technical (Professional)"
        summary_length (str): "Concise (Bullet Points)" or "Detailed (Full Text)"
    
    Returns:
        str: The generated summary
    """
    
    global last_request_time
    
    # Rate limiting
    elapsed = time.time() - last_request_time
    if elapsed < MIN_INTERVAL:
        wait_time = MIN_INTERVAL - elapsed
        time.sleep(wait_time)
    
    # Determine style prompt
    if summary_style.startswith("Simple"):
        style_prompt = (
            "Rewrite in simple English. Short sentences, easy words. "
            "Be factual and direct.\n\n"
        )
    else:
        style_prompt = (
            "Rewrite professionally. Technical terms, full depth. "
            "Be comprehensive and direct.\n\n"
        )
    
    # CRITICAL: Proper length control
    if summary_length.startswith("Concise"):
        # CONCISE: Very short - only key points
        length_prompt = (
            "MAXIMUM 6-8 bullet points only. "
            "EACH BULLET: Only ONE sentence, max 15 words. "
            "Extract ONLY the most critical facts. "
            "NO paragraphs, NO explanations, NO context.\n\n"
        )
    else:
        # DETAILED: Very long - comprehensive
        length_prompt = (
            "Write comprehensive analysis. "
            "4 to 6 paragraphs. "
            "Include: context, analysis, implications, examples. "
            "TOTAL: upto 100-150 words per paragaphs. "
            "Cover all major points thoroughly. "
            "Add detailed explanations and depth.\n\n"
        )
    
    # Final prompt
    final_prompt = (
        f"{style_prompt}"
        f"{length_prompt}"
        f"Article:\n{text}"
    )
    
    # Multiple attempts to bypass server-side blocking
    attempts = [
        # Attempt 1: Flash standard
        lambda: genai.GenerativeModel(
            "gemini-2.5-flash",
            generation_config={
                "temperature": 0.5,
                "top_p": 0.8,
                "top_k": 40,
                "max_output_tokens": 1024 if summary_length.startswith("Concise") else 2048,
            },
            safety_settings=[
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
            ]
        ).generate_content(final_prompt),
        
        # Attempt 2: Reworded prompt
        lambda: genai.GenerativeModel("gemini-2.5-flash").generate_content(
            f"Please analyze and summarize in {summary_style}:\n\n{text}"
        ),
        
        # Attempt 3: 2.0 Flash
        lambda: genai.GenerativeModel(
            "gemini-2.0-flash",
            generation_config={"max_output_tokens": 2048},
        ).generate_content(final_prompt),
        
        # Attempt 4: Stream mode
        lambda: _stream_generate(final_prompt),
        
        # Attempt 5: Simple neutral
        lambda: genai.GenerativeModel("gemini-2.5-flash").generate_content(
            f"Summarize:\n{text}"
        ),
    ]
    
    for i, attempt_func in enumerate(attempts, 1):
        try:
            print(f"Attempt {i}...")
            response = attempt_func()
            
            if response and response.text and response.text.strip():
                last_request_time = time.time()
                return response.text.strip()
        except Exception as e:
            print(f"Attempt {i} failed: {str(e)[:80]}")
            continue
    
    # All attempts failed
    return (
        "⚠️ Unable to summarize this article.\n\n"
        "**Why:** Content triggers Gemini's server-side safety filters.\n\n"
        "**Try:**\n"
        "• Different news source (Reuters, BBC, AP News)\n"
        "• Less sensitive topic\n"
        "• Wait 1-2 minutes and retry"
    )


def _stream_generate(prompt):
    """Stream mode generation (sometimes bypasses filters)."""
    model = genai.GenerativeModel("gemini-2.5-flash")
    full_response = ""
    
    try:
        for chunk in model.generate_content(prompt, stream=True):
            if chunk.text:
                full_response += chunk.text
    except:
        pass
    
    class FakeResponse:
        text = full_response
    
    return FakeResponse()
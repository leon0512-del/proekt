import os
import time
from google import genai


MY_API_KEY = os.getenv("GEMINI_API_KEY", "ТВОЈОТ_КЛУЧ_ТУКА")
client = genai.Client(api_key=MY_API_KEY)

def generate_hint(game_type, existing_hints):
    prompt = f"I am playing a guessing game for a {game_type}. The current hints are: {existing_hints}. Give me one new short hint."

    max_retries = 3
    for attempt in range(max_retries):
        try:

            response = client.models.generate_content(
                model="gemini-3-flash",
                contents=prompt
            )
            return response.text.strip()
        except Exception as e:
            print(f"Attempt {attempt+1} failed: {e}")
            if "429" in str(e):
                time.sleep(2)
                continue
            return "AI couldn't think of a hint right now."
    return "AI Rate limit reached."

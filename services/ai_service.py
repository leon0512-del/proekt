import time
from google import genai
from google.genai import types


MY_API_KEY = ""

client = genai.Client(api_key=MY_API_KEY)


def generate_hint(game_type, existing_hints):
    prompt = f"""
    I am playing a guessing game for a {game_type}.
    The current hints are: {existing_hints}.
    Give me one new short hint that does not reveal the answer.
    """


    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model="gemini-3-flash-preview",
                contents=prompt
            )
            return response.text.strip()

        except Exception as e:
            print(e)

            if "429" in str(e) or "Resource exhausted" in str(e):
                print(f"Rate limit hit. Waiting... (Attempt {attempt + 1}/{max_retries})")
                time.sleep(2)  # Wait 2 seconds before trying again
            else:

                print(f"AI Error: {e}")
                return "AI Service Unavailable"

    return "AI is busy (Rate Limit). Pocekaj moment leo."

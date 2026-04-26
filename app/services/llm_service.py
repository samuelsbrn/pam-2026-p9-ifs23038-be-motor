import requests
from app.config import Config


def generate_from_llm(prompt: str):
    if not Config.BASE_URL:
        raise Exception("LLM_BASE_URL is not configured")

    if not Config.LLM_TOKEN:
        raise Exception("LLM_TOKEN is not configured")

    response = requests.post(
        Config.BASE_URL,
        params={"key": Config.LLM_TOKEN},
        json={
            "contents": [
                {
                    "parts": [
                        {
                            "text": prompt
                        }
                    ]
                }
            ]
        },
        timeout=30,
    )

    if response.status_code != 200:
        raise Exception(f"LLM request failed: {response.status_code} - {response.text}")

    return response.json()

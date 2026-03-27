# backend/llm/llm_client.py

from groq import Groq
from config.settings import settings
import json
import re

client = Groq(api_key=settings.GROQ_API_KEY)


def extract_json(text: str) -> dict:
    """
    Extract JSON from LLM output (since Groq doesn't enforce it)
    """
    try:
        return json.loads(text)
    except:
        # Try to extract JSON block
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            return json.loads(match.group())
        else:
            raise ValueError(f"Could not extract JSON:\n{text}")


def call_llm(prompt: str, system_prompt: str = None) -> dict:
    if not settings.GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY missing in .env")

    messages = []

    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})

    messages.append({
        "role": "user",
        "content": prompt + "\n\nIMPORTANT: Return ONLY valid JSON."
    })

    response = client.chat.completions.create(
        model=settings.LLM_MODEL,
        messages=messages,
        temperature=0.2  # 🔥 keep low for consistency
    )

    content = response.choices[0].message.content

    return content
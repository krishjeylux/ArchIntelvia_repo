# backend/config/settings.py

import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    # 🔑 API Keys
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

    # 🤖 Model
    
    LLM_MODEL = os.getenv("LLM_MODEL", "llama-3.1-8b-instant")
    # ⚙️ RAG
    TOP_K = 3

    DEBUG = True


settings = Settings()
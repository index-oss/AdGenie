from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = Path(__file__).resolve().parent / "data"

PROJECT_TITLE = "AdGenie API: AI-Powered Recommendations & Regional Ad Generation"
PROJECT_DESCRIPTION = (
    "A plug-and-play Python API enabling any e-commerce platform to serve "
    "context-aware ML product recommendations and dynamically localized regional ads."
)
VERSION = "1.0.0"

# Monetization Defaults
DEFAULT_CPC = 22.50       # Avg Cost-per-click in INR (₹22.50)
AFFILIATE_RATE = 0.08     # 8% avg affiliate commission on checkout
STATIC_BASELINE_CTR = 1.8 # 1.8% baseline static ad CTR

SUPPORTED_LANGUAGES = {
    "en": "English",
    "hi": "Hindi",
    "hinglish": "Hinglish",
    "pa": "Punjabi",
    "mr": "Marathi",
    "bn": "Bengali",
    "ta": "Tamil",
    "te": "Telugu"
}

# Optional external LLM key, otherwise graceful creative offline heuristic engine is used
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

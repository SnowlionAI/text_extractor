import os
from dotenv import load_dotenv

# Load .env variables if available
load_dotenv()

# OpenAI API Key (from .env or system environment variables)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your-fallback-api-key")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "your-fallback-api-key")

# OpenAI Model (default to GPT-4)
#MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")
MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-pro-exp-02-05")

# Supported programming languages (file extensions)
SUPPORTED_EXTENSIONS = [
    ".py",  # Python
    ".js",  # JavaScript
    ".java",  # Java
    ".cpp",  # C++
    ".html",  # HTML
    ".ts",  # TypeScript
    ".cs",  # C#
    ".php",  # PHP
    ".vue",  # Vue  
]

RATE_LIMIT_RPD = int(os.getenv("RATE_LIMIT_RPD", "1000000"))
RATE_LIMIT_RPM = int(os.getenv("RATE_LIMIT_RPM", "1000000"))
MINIMUM_WAIT_SECONDS = float(os.getenv("MINIMUM_WAIT_SECONDS", "0.1"))


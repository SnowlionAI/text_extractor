import os
from dotenv import load_dotenv

# Load .env variables if available
load_dotenv()

# OpenAI API Key (from .env or system environment variables)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your-fallback-api-key")

# OpenAI Model (default to GPT-4)
MODEL = os.getenv("OPENAI_MODEL", "gpt-4")

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
]


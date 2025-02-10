from typing import Dict, Any
import json
import jsonschema
from openai import OpenAI
import os
import google.generativeai as genai

from text_extractor.config import OPENAI_API_KEY, GEMINI_API_KEY, MODEL, SUPPORTED_EXTENSIONS
from text_extractor.prompt import SYSTEM_PROMPT  # Import the system prompt
from text_extractor.extractor_tool import EXTRACTOR_TOOL

from text_extractor.ai.openai import process_with_openai
from text_extractor.ai.gemini import process_with_opengemini


def process_ai(
    model: str,
    system_prompt: str,
    source_code: str,
    extractor_tool: list,
    schema: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Process source code using OpenAI or Gemini's API to extract and translate text.

    Args:
        model (str): The AI model to use.
        system_prompt: The system prompt to guide the AI.
        source_code: The source code to process.
        extractor_tool: The tool definition for extraction.
        schema: JSON schema for validation.

    Returns:
        Dict containing translations and modified code
    """
    if model.startswith("gemini"):
        return process_with_opengemini(
            model=model,
            system_prompt=system_prompt,
            source_code=source_code,
            extractor_tool=extractor_tool,
            schema=schema
        )
    else:
        return process_with_openai(
            model=model,
            system_prompt=system_prompt,
            source_code=source_code,
            extractor_tool=extractor_tool,
            schema=schema
        )

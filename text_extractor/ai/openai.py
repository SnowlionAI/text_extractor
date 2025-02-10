from typing import Dict, Any
import json
import jsonschema
from openai import OpenAI

from text_extractor.config import OPENAI_API_KEY, MODEL, SUPPORTED_EXTENSIONS
from text_extractor.prompt import SYSTEM_PROMPT  # Import the system prompt
from text_extractor.extractor_tool import EXTRACTOR_TOOL

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)



def process_with_openai(
    model: str,
    system_prompt: str,
    source_code: str,
    extractor_tool: list,
    schema: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Process source code using OpenAI's API to extract and translate text.
    
    Args:
        client: OpenAI client instance
        model: The OpenAI model to use
        system_prompt: The system prompt to guide the AI
        source_code: The source code to process
        extractor_tool: The tool definition for extraction
        schema: JSON schema for validation
        
    Returns:
        Dict containing translations and modified code
    """
    client = OpenAI(api_key=OPENAI_API_KEY)

    # Send request to ChatGPT
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {"role": "user", "content": source_code}
        ],
        tools=extractor_tool,
        tool_choice={"type": "function", "function": {"name": "process_source"}}
    )

    # Parse response
    tool_call = response.choices[0].message.tool_calls[0]
    output = json.loads(tool_call.function.arguments)

    # print(f"processed translations: {output['translations']}")
    # print(f"processed modified_code: {output['modified_code']}")
    
    # Validate output against schema
    jsonschema.validate(instance=output, schema=schema)
    
    return output

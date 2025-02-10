import os
import google.generativeai as genai
import json
from typing import Dict, Any

from text_extractor.config import GEMINI_API_KEY, MODEL, SUPPORTED_EXTENSIONS
from text_extractor.prompt import SYSTEM_PROMPT  # Import the system prompt
from text_extractor.extractor_tool import EXTRACTOR_TOOL


genai.configure(api_key=GEMINI_API_KEY)

# Create the model
# generation_config = {
#   "temperature": 0.7,
#   "top_p": 0.95,
#   "top_k": 64,
#   "max_output_tokens": 131072,
#   "response_mime_type": "text/plain",
# }

def process_with_opengemini(
    model: str,
    system_prompt: str,
    source_code: str,
    extractor_tool: list,
    schema: Dict[str, Any]
) -> Dict[str, Any]:

    tools = [
        {'code_execution': {}},
        {'function_declarations': [extractor_tool[0]['function']]}
    ]

    generation_config = {
        "temperature": 0.1,  # Lower temperature for more consistent output
        "top_p": 1,
        "top_k": 1,
        "max_output_tokens": 131072,
        "candidate_count": 1,
    }



    model = genai.GenerativeModel(
        model_name=model,
        generation_config=generation_config,
        # system_instruction="You are a code transformation assistant. \n\n- Extract all user-facing translatable text from the given source code.Ensure UI elements, buttons, labels, tooltips, and messages are included while excluding logs, debug messages,and internal variables. \n\n- For each translatable text: \n    - create a globally unique hash value / uuid based on the translatable text containing at least 8 characters, e.g. `a01b1234`  \n    - Replace the original translatable text with a function call `$t(<hash/uuid>)` or similar function call, adjusted to the programming language.\n    - Ensure the $t('uuid') function is properly placed to keep the original intended output as close as possible. E.g.: replace\n        `print(f\"processing: {file_path}\")` with `print(f\"{$t(<uuid>)}: {file_path}\")`\n    - Place the original text as a comment next in suitable place in the replaced text. E.g. in Vue templates this means right \n- Return the modified source code and the extracted translations and uuids in a property escaped JSON object.\n- Do not include any markdown formatting or additional commentary in the response.\n\n\nSpecifically for Vue templates files:\n\nIMPORTANT: Replace the original translatable text with a function call `{{$t(<hash/uuid>)}}`\nIMPORTANT: In the template part: \n- Place the original text as a comment just above to the <v-text-field> tag.\n- Use a colon (:) in the template when binding a property or attribute to a dynamic JavaScript expression, such as \"$t(<id>)\".\n- Use double curly braces ({{ }}) to interpolate a JavaScript expression directly into the DOM text.\n\nIMPORTANT: In the <script> part:\n-  the translatable dynamic text should be replaced like so: this.$t(<id>)\n\n\nSpecifically for javascript and js files:\n\n- At the top of the file add the line, after the other import statements, add the import statement: import i18n from \"@/i18n\";\n\n- All translatable dynamic text should be replaced like so: i18n.global.t(<id>)\n",
        system_instruction=system_prompt,
        # tools=tools,
        # tool_config={
        #     "function_calling_config": {
        #         "mode": "ANY",
        #         "allowed_function_names": ["process_source"]
        #     }
        # }
    )

    chat_session = model.start_chat(
    history=[
    ]
    )
    response = chat_session.send_message(source_code)

    try:
        # Try to get the response directly if it's already JSON
        if hasattr(response, 'json'):
            return response.json()
        
        # Clean and parse the text response
        text = response.text.strip()
        if text.startswith('```json'):
            text = text[7:]
        if text.endswith('```'):
            text = text[:-3]
        
        return json.loads(text)
    except (json.JSONDecodeError, AttributeError) as e:
        print(f"Error decoding JSON: {str(e)}\nResponse: {response.text}")
        return {"error": f"Failed to decode JSON from the response: {str(e)}"}

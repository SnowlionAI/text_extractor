from openai import OpenAI
import os
import json
import hashlib
import jsonschema
from text_extractor.config import OPENAI_API_KEY, MODEL, SUPPORTED_EXTENSIONS
from text_extractor.prompt import SYSTEM_PROMPT  # Import the system prompt
from text_extractor.extractor_tool import EXTRACTOR_TOOL

schema = {
    "type": "object",
    "properties": {
        "modified_code": {"type": "string"},
        "translations": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "string"},
                    "original_text": {"type": "string"}
                },
                "required": ["id", "original_text"]
            }
        }
    },
    "required": ["modified_code", "translations"]
}

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# Function to generate a unique ID for translation keys
def generate_id(text):
    return hashlib.md5(text.encode()).hexdigest()[:8]

# Function to process a single file
def process_file(file_path):
    print(f"processing: {file_path}")
    with open(file_path, "r", encoding="utf-8") as f:
        source_code = f.read()

    # Send request to ChatGPT
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {"role": "user", "content": source_code}
        ],
        tools=EXTRACTOR_TOOL,
        tool_choice={"type": "function", "function": {"name": "process_source"}}
    )

    # Parse response
    tool_call = response.choices[0].message.tool_calls[0]
    output = json.loads(tool_call.function.arguments)
    print(f"processed translations: {output['translations']}")
    print(f"processed modified_code: {output['modified_code']}")
    jsonschema.validate(instance=output, schema=schema)

    modified_code = output["modified_code"]
    translations = output["translations"]

    print(f"processed: {file_path}")
    return modified_code, translations

# Function to process an entire directory
def process_directory(directory, output_json="translations.json", output_directory="outputdir"):
    all_translations = {}

    for root, _, files in os.walk(directory):
        for file in files:
            # Only process files with supported extensions
            if any(file.endswith(ext) for ext in SUPPORTED_EXTENSIONS):
                original_file_path = os.path.join(root, file)
                # Compute the file's relative path from the starting directory
                relative_path = os.path.relpath(original_file_path, start=directory)
                # Determine where the file will be saved in the output directory
                new_file_path = os.path.join(output_directory, relative_path)

                # Check if the modified file already exists in the output directory
                if os.path.exists(new_file_path):
                    print(f"Skipping existing file: {new_file_path}")
                    continue

                # Process the file
                modified_code, translations = process_file(original_file_path)

                # Ensure the target directory exists
                os.makedirs(os.path.dirname(new_file_path), exist_ok=True)

                # Save the modified code to the new location
                with open(new_file_path, "w", encoding="utf-8") as f:
                    f.write(modified_code)

                # Merge translations from this file into the overall dictionary
                for item in translations:
                    all_translations[item["id"]] = {
                        "original_text": item["original_text"],
                        "filename": f"{relative_path}"
                    }
    # Save all translations to a JSON file
    # Load existing translations if the output file already exists

    output_json_file = os.path.join(output_directory, output_json)

    if os.path.exists(output_json_file):
        with open(output_json_file, "r", encoding="utf-8") as f:
            existing_data = json.load(f)
    else:
        existing_data = {}

    # Merge the new translations with the existing ones
    existing_data.update(all_translations)

    # Write the merged data back to the file
    with open(output_json_file, "w", encoding="utf-8") as f:
        json.dump(existing_data, f, indent=4, ensure_ascii=False)

    print(f"✅ Processing complete. Modified files are saved under '{output_directory}', and translations are saved to '{output_json_file}'.")
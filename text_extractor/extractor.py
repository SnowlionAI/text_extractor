import os
import json
import hashlib
import jsonschema
from text_extractor.config import MODEL, SUPPORTED_EXTENSIONS
from text_extractor.prompt import SYSTEM_PROMPT  # Import the system prompt
from text_extractor.extractor_tool import EXTRACTOR_TOOL

from text_extractor.replace_check import check_replace

import time

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

import uuid
generation_id = uuid.uuid4().hex[:8]


print(f"Using model '{MODEL}'")

# Initialize OpenAI client
# client = OpenAI(api_key=OPENAI_API_KEY)

# Function to generate a unique ID for translation keys
def generate_id(text):
    return hashlib.md5(text.encode()).hexdigest()[:8]

# Function to process a single file
def process_file(file_path):
    print(f"processing: {file_path}")
    with open(file_path, "r", encoding="utf-8") as f:
        source_code = f.read()

    from text_extractor.ai.ai import process_ai
    
    output = process_ai(
        model=MODEL,
        system_prompt=SYSTEM_PROMPT,
        source_code=source_code,
        extractor_tool=EXTRACTOR_TOOL,
        schema=schema
    )

    try:
        modified_code = output["modified_code"]
        translations = output["translations"]
    except KeyError as e:
        print(f"Error: Could not find expected key '{e.args[0]}' in output of file: {file_path}")
        return None, None

    print(f"processed: {file_path}")
    return modified_code, translations

# Function to process an entire directory
def process_directory(directory_root, output_json="translations.json", output_directory="outputdir", subdir=""):
    all_translations = {}

    # Walk the directory structure
    directory = os.path.join(directory_root, subdir)

    print(f"\n✅ Processing directory '{directory}'")

    for root, _, files in os.walk(directory):
        for file in files:
            # Only process files with supported extensions
            if any(file.endswith(ext) for ext in SUPPORTED_EXTENSIONS):
                original_file_path = os.path.join(root, file)
                # Compute the file's relative path from the starting directory
                relative_path = os.path.relpath(original_file_path, start=directory)
                # Determine where the file will be saved in the output directory
                new_file_path = os.path.join(output_directory, subdir,relative_path)

                # Check if the modified file already exists in the output directory
                if os.path.exists(new_file_path):
                    print(f"Skipping existing file: {new_file_path}")
                    continue

                # if not check_replace(original_file_path):
                #     print(f"Skipping no hardcoded text file: {new_file_path}")
                #     continue

                # print(f"Processing file: {new_file_path}")

                # Process the file

                try:
                    modified_code, translations = process_file(original_file_path)
                except Exception as e:
                    print(f"Error: Could not process file: {original_file_path}. Error: {e}")
                    # time.sleep(30)
                    continue
                if modified_code is None or translations is None:
                    # time.sleep(30)
                    continue
                
                # time.sleep(30)
                # Wait for 30 seconds to avoid rate limiting

                # Ensure the target directory exists
                os.makedirs(os.path.dirname(new_file_path), exist_ok=True)

                # Save the modified code to the new location
                with open(new_file_path, "w", encoding="utf-8") as f:
                    f.write(modified_code)

                # Merge translations from this file into the overall dictionary
                for item in translations:
                    all_translations[item["id"]] = {
                        "original_text": item["original_text"],
                        "original_filename": f"{original_file_path}",
                        "new_filename": f"{new_file_path}",
                        "generation_id": f"{generation_id}"
                    }
 
                # Save all translations to a JSON file
            
                output_json_file = os.path.join(output_directory, output_json)

                # Load existing data or initialize an empty dictionary
                existing_data = {}
                if os.path.exists(output_json_file):
                    with open(output_json_file, "r", encoding="utf-8") as f:
                        existing_data = json.load(f)

                # Filter out entries with the same original_filename
                updated_data = {
                    key: value
                    for key, value in existing_data.items()
                        if value.get("original_filename") != original_file_path # Use .get() to avoid KeyError if "filename" key is missing
                }

                # Update with new translations
                updated_data.update(all_translations)

                # Write the merged data back to the file
                with open(output_json_file, "w", encoding="utf-8") as f:
                    json.dump(updated_data, f, indent=4, ensure_ascii=False)
                    print(f"✅ Processing complete. Modified files are saved under '{output_directory}', and translations are saved to '{output_json_file}'.")


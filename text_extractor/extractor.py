import openai
import os
import json
import hashlib
from text_extractor.config import OPENAI_API_KEY, MODEL

# Set OpenAI API key
openai.api_key = OPENAI_API_KEY

# Function to generate a unique ID for translation keys
def generate_id(text):
    return hashlib.md5(text.encode()).hexdigest()[:8]

# Function to process a single file
def process_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        source_code = f.read()

    # Send request to ChatGPT
    response = openai.ChatCompletion.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "Extract all user-facing translatable text from the given source code "
                    "and replace them with `translate('id')`. Ensure UI elements, "
                    "buttons, labels, tooltips, and messages are included while excluding logs."
                )
            },
            {"role": "user", "content": source_code}
        ]
    )

    # Parse response
    output = json.loads(response["choices"][0]["message"]["content"])
    modified_code = output["modified_code"]
    translations = output["translations"]

    # Save modified source code
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(modified_code)

    return translations

# Function to process an entire directory
def process_directory(directory, output_json="translations.json"):
    all_translations = {}

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith((".py", ".js", ".java", ".cpp", ".html")):  # Add relevant extensions
                file_path = os.path.join(root, file)
                translations = process_file(file_path)
                
                # Store translations in dictionary format
                for item in translations:
                    all_translations[item["id"]] = item["original_text"]

    # Save translations to JSON file
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(all_translations, f, indent=4, ensure_ascii=False)

    print(f"✅ Processing complete. Source files updated, translations saved to {output_json}.")

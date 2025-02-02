
EXTRACTOR_TOOL = [
    {
        "type": "function",
        "function": {
            "name": "process_source",
            "description": "Extract translatable texts and replace with translate('id').",
            "parameters": {
                "type": "object",
                "properties": {
                    "modified_code": {"type": "string", "description": "The updated source code."},
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
        }
    }
]
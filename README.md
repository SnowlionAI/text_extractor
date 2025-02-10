# Text Extractor - CLI Tutorial

## Overview
Text Extractor is a command-line tool that helps you extract and internationalize hardcoded text from your source code files. It processes your files, generates unique IDs for text strings, and creates a translations JSON file while preserving the original code structure.

## Features
- **Replaces hardcoded text** with `translate(<id>)`
- **Stores extracted texts** in `translations.json`
- **Ignores logs, debug messages,** and internal variables
- **Supports multiple programming languages** (default: Python, JavaScript, Java, C++, HTML, etc.) – configurable in `config.py`
- **Adjustable through the systems prompt** Easily adjust processing and output via the system prompt (see `prompt.py`)
- **Works via CLI or as a Python module**
- **Saves modified source files** to a separate output directory (default: `modified_sources`), preserving the complete relative path
- **Skips files** that have already been processed and exist in the output directory


## Prerequisites
- Python 3.x
- OpenAI API key (set in `.env` file) 
or a 
- Gemini API key (set in `.env` file)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd text_extractor
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure your OpenAI API key in `.env`:
```bash
OPENAI_API_KEY=your-api-key-here
```

or 

3. Configure your Gemini API key in `.env`:
```bash
GEMINI_API_KEY=your-gemini-api-key-here
```

## Basic Usage

The basic command structure is:
```bash
python -m text_extractor.cli <source_directory> [options]
```

### Command Arguments

- `directory`: Path to the source code directory (required)
- `--outputdir`: Output directory for processed files (default: "outputdir")
- `--subdir`: Specific subdirectories to process within `directory` (default: "")
- `--output`: Output file for translations (default: "translations.json")

### Examples

1. Process a single directory:
```bash
python -m text_extractor.cli ./src/components --outputdir ./output
```

2. Process specific subdirectories:
```bash
python -m text_extractor.cli ./src --outputdir ./output --subdir "components,pages"
```

3. Process multiple subdirectories with custom output:
```bash
python -m text_extractor.cli ./src \
  --outputdir ./output/components \
  --subdir "AccountSettings,Auth,Card" \
  --output custom-translations.json
```

## Output Structure

### 1. Processed Files
The tool creates a mirror of your source directory structure in the output directory with processed files. Each processed file will have its hardcoded strings replaced with translation function calls.

Example:
```
Original: <h1>Welcome to our site</h1>
Processed: <h1>{{ $t('a1b2c3d4') }}</h1>
```

### 2. Translations File
A JSON file containing all extracted texts with their corresponding IDs:
```json
{
    "a1b2c3d4": {
        "original_text": "Welcome to our site",
        "original_filename": "/path/to/original/file",
        "new_filename": "/path/to/processed/file",
        "generation_id": "unique-id"
    }
}
```

## Best Practices

1. **Backup Your Code**: Always work on a copy of your source code or use version control.

2. **Start Small**: Test with a small directory first to understand the output format.

3. **Review Translations**: Always review the generated translations.json file to ensure accuracy.

4. **Incremental Processing**: Process your codebase in smaller chunks using the `--subdir` option.

## Error Handling

The tool provides error messages for common issues:
- Missing API keys
- Invalid file paths
- Processing errors for specific files
- Rate limiting warnings

## Limitations

- Currently supports Vue template files
- Processes text within specific code contexts
- Rate limiting may apply based on your OpenAI API plan

## Support

For issues or questions, please:
1. Check the error messages in the console output
2. Verify your API key configuration
3. Ensure your source files are in a supported format

## Contributing

Contributions are welcome! Please feel free to submit pull requests or create issues for bugs and feature requests.

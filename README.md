# Text Extractor

Text Extractor is a Python tool that scans source code, extracts user-facing hardcoded text, and replaces it with a `translate("id")` function.

## Features
- **Replaces hardcoded text** with `translate("id")`
- **Stores extracted texts** in `translations.json`
- **Ignores logs, debug messages,** and internal variables
- **Supports multiple programming languages** (default: Python, JavaScript, Java, C++, HTML, etc.) – configurable in `config.py`
- **Works via CLI or as a Python module**
- **Saves modified source files** to a separate output directory (default: `modified_sources`), preserving the complete relative path
- **Skips files** that have already been processed and exist in the output directory

---

## Installation
Clone and install:
<pre>
```bash
git clone https://github.com/yourgithub/text-extractor.git
# add your OpenAI API key to .env
cd text-extractor
pip install .
</pre>

## Customizing the System Prompt
If you want to fine-tune how the AI extracts and replaces translatable text, edit prompt.py inside the text_extractor directory.

## Customizing Supported File Types
To add or remove supported programming languages, edit config.py inside the text_extractor directory.

## Usage
Command-Line Interface (CLI)

Processing a Directory:

By default, the tool scans the given source directory, processes all supported source files, and saves:

- Modified files to a separate output directory (outputdir by default) while preserving their relative paths.
- Extracted translations to a JSON file in the output directory (translations.json by default).

<pre>
```bash
text-extractor /path/to/source/code
</pre>

## To specify an output file:

<pre>
```bash
text-extractor /path/to/source/code --output my_translations.json --outputdir my_outputdir
</pre>

## Run Without Installing the Package
<pre>
```bash
python -m text_extractor.cli .
</pre>


## Python API
To use the package in a Python script:

<pre>
```python
from text_extractor.extractor import process_directory

process_directory("path/to/source/code", "translations.json")
</pre>
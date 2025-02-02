# Text Extractor

Text Extractor is a Python tool that scans source code, extracts user-facing hardcoded text, and replaces it with a `translate("id")` function.

## Features
✅ Replaces hardcoded text with `translate("id")`  
✅ Stores extracted texts in `translations.json`  
✅ Ignores logs, debug messages, and internal variables  
✅ Supports **Python, JavaScript, Java, C++, and HTML**  
✅ Works via CLI **or** as a Python module  

---

## Installation
Clone and install:
<pre>
```bash
git clone https://github.com/yourgithub/text-extractor.git
cd text-extractor
pip install .
</pre>
---

## Usage
Command-Line Interface (CLI)
To process a directory:

<pre>
```bash
text-extractor /path/to/source/code
</pre>

## To specify an output file:

<pre>
```bash
text-extractor /path/to/source/code --output my_translations.json
</pre>

## Python API
To use the package in a Python script:

<pre>
```python
from text_extractor.extractor import process_directory

process_directory("path/to/source/code", "translations.json")
</pre>
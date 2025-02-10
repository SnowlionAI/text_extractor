import os
import json
import re
import hashlib

pattern = re.compile(
    r'(<([a-zA-Z0-9-]+)[^>]*>)'
    r'([^<{]+?)'
    r'(\{\{[^}]*\}\}[^<{]*?)?'
    r'(</\2>)',
    re.DOTALL
)

attribute_exclusion_pattern = re.compile(
    r"(@click|@change|@focus|@input|@keydown|function|=>|\(\)|\[.*?\]|:append)"
)

def generate_id(text: str) -> str:
    return "t_" + hashlib.md5(text.encode()).hexdigest()[:8]

def unify_linebreaks(text: str) -> str:
    text = text.replace("\n", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def looks_like_code(text: str) -> bool:
    suspicious_tokens = ["=>", "()", ";", "@click"]

    txt = text.strip()

    if re.search(r"\?\.[a-zA-Z_]", txt):
        return True

    if ">" in txt:
        if ">{{" not in txt and re.search(r">\S", txt):
            return True

    for token in suspicious_tokens:
        if token in txt:
            return True

    if re.search(r"\{(?!\{)", txt):
        return True
    if re.search(r"(?!\})\}", txt):
        return True

    return False

def needs_replacement(match: re.Match) -> bool:
    opening_tag, tag_name, hardcoded_text, interpolation, closing_tag = match.groups()

    if not hardcoded_text.strip():
        return False

    if attribute_exclusion_pattern.search(opening_tag):
        return False

    if looks_like_code(hardcoded_text):
        return False

    cleaned_text = unify_linebreaks(hardcoded_text)
    if not cleaned_text:
        return False

    return True

def replace_text(match: re.Match) -> str:
    opening_tag, tag_name, hardcoded_text, interpolation, closing_tag = match.groups()

    if not hardcoded_text.strip():
        return match.group(0)

    if attribute_exclusion_pattern.search(opening_tag):
        return match.group(0)

    if looks_like_code(hardcoded_text):
        return match.group(0)

    cleaned_text = unify_linebreaks(hardcoded_text)
    if not cleaned_text:
        return match.group(0)

    text_id = generate_id(cleaned_text)
    # translations["en"][text_id] = cleaned_text

    new_text = f"{{{{ $t('{text_id}') }}}}"

    if interpolation:
        new_text += f" {interpolation}"

    return f"{opening_tag}{new_text}{closing_tag}"



# def replace_text(match: re.Match) -> str:
#     opening_tag, tag_name, hardcoded_text, interpolation, closing_tag = match.groups()

#     if not needs_replacement(match):
#         return match.group(0)

#     text_id = generate_id(unify_linebreaks(hardcoded_text))
#     translations["en"][text_id] = unify_linebreaks(hardcoded_text)

#     new_text = f"{{{{ $t('{text_id}') }}}}"

#     if interpolation:
#         new_text += f" {interpolation}"

#     return f"{opening_tag}{new_text}{closing_tag}"


def check_replace(file_path):
    content = None
    replaced_content = None

    if file_path.endswith(".vue"):
        print(f"checking: {file_path}")
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        replaced_content = re.sub(pattern, replace_text, content)

        not_equal = replaced_content != content

        return not not_equal

    elif file_path.endswith(".js"):
        return True

    return False

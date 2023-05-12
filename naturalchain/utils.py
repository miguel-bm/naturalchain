import re
from datetime import datetime
from pathlib import Path


def extract_first_code_block(text: str) -> str:
    pattern = r"```(?:[a-zA-Z0-9]+)?\n(.*?)\n```"
    match = re.search(pattern, text, re.DOTALL)

    if match:
        return match.group(1)
    raise ValueError("No code block found in text.")


def preprocess_solidity_code(code: str) -> str:
    return code.replace("pragma solidity ^0.8.0;", "pragma solidity 0.8.19;")


def save_to_text_file(text: str, file_location: Path, file_name: str):
    file_location.mkdir(parents=True, exist_ok=True)
    file_path = file_location / file_name
    with file_path.open("w") as f:
        f.write(text)


def get_datetime_string() -> str:
    return datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

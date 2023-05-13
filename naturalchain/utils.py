import re
from datetime import datetime
from pathlib import Path
from typing import Literal

from decouple import config
from web3 import Web3


def extract_first_code_block(text: str) -> str:
    pattern = r"```(?:[a-zA-Z0-9]+)?\n(.*?)\n```"
    match = re.search(pattern, text, re.DOTALL)

    if match:
        return match.group(1)
    raise ValueError("No code block found in text.")


def preprocess_solidity_code(code: str) -> str:
    code.replace(
        "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/",
        "@openzeppelin",
    )
    return code.replace("pragma solidity ^0.8.0;", "pragma solidity 0.8.19;")


def save_to_text_file(text: str, file_location: Path, file_name: str):
    file_location.mkdir(parents=True, exist_ok=True)
    file_path = file_location / file_name
    with file_path.open("w") as f:
        f.write(text)


def get_datetime_string() -> str:
    return datetime.now().strftime("%Y-%m-%d-%H-%M-%S")


def camel_to_snake(string):
    # Insert an underscore before any capital letters and convert to lowercase
    snake_case = re.sub(r"(?<!^)(?=[A-Z])", "_", string).lower()
    return snake_case


INFURA_API_KEY = config("INFURA_API_KEY")

NETWORK_RPC_ENDPOINTS = {
    "ethereum_mainnet": f"https://mainnet.infura.io/v3/{INFURA_API_KEY}",
    "near_mainnet": f"https://near-mainnet.infura.io/v3/{INFURA_API_KEY}",
    "avalanche_mainnet": f"https://avalanche-mainnet.infura.io/v3/{INFURA_API_KEY}",
}

NETWORKS = Literal[tuple(NETWORK_RPC_ENDPOINTS.keys())]  # type: ignore


def get_web3(network: str) -> Web3:
    try:
        endpoint = NETWORK_RPC_ENDPOINTS[network]
        return Web3(Web3.HTTPProvider(endpoint))
    except KeyError:
        raise ValueError(f"Unsupported network: {network}")

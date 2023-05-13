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
    code = code.replace(
        "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/",
        "@openzeppelin",
    )
    code = code.replace("pragma solidity 0.8.9;", "pragma solidity 0.8.19;")
    code = code.replace("pragma solidity ^0.8.0;", "pragma solidity 0.8.19;")
    code = code.replace(
        "ERC20/extensions/ERC20Permit.sol", "ERC20/extensions/draft-ERC20Permit.sol"
    )
    return code


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
    "ethereum_sepolia": f"https://sepolia.infura.io/v3/{INFURA_API_KEY}",
    "ethereum_goerli": f"https://goerli.infura.io/v3/{INFURA_API_KEY}",
    "polygon_mainnet": f"https://polygon-mainnet.infura.io/v3/{INFURA_API_KEY}",
    "polygon_mumbai": f"https://polygon-mumbai.infura.io/v3/{INFURA_API_KEY}",
    "optimism_mainnet": f"https://optimism-mainnet.infura.io/v3/{INFURA_API_KEY}",
    "optimism_goerli": f"https://optimism-goerli.infura.io/v3/{INFURA_API_KEY}",
    "gnosis_mainnet": f"https://rpc.gnosis.gateway.fm",
    "gnosis_chiado": f"https://rpc.chiado.gnosis.gateway.fm",
    "linea_goerli": f"https://rpc.goerli.linea.build",
    "scroll_goerli": f"https://alpha-rpc.scroll.io/l2",
    "neon_devnet": f"https://devnet.neonevm.org",
    "mantle_testnet": f"https://rpc.testnet.mantle.xyz/",
}

CMC_NETWORK_NAMES = {
    "ethereum_mainnet": "Ethereum",
    "ethereum_sepolia": "Ethereum Sepolia",
    "ethereum_goerli": "Ethereum Goerli",
    "polygon_mainnet": "Polygon",
    "polygon_mumbai": "Polygon Mumbai",
    "optimism_mainnet": "Optimism Mainnet",
    "optimism_goerli": "Optimism Goerli",
    "gnosis_mainnet": "Gnosis",
    "gnosis_chiado": "Gnosis Chiado",
    "linea_goerli": "Linea Goerli",
    "scroll_goerli": "Scroll",
    "neon_devnet": "Neon Devnet",
    "mantle_testnet": "Mantle Testnet",
}

NETWORKS = Literal[
    "ethereum_mainnet",
    "ethereum_sepolia",
    "ethereum_goerli",
    "polygon_mainnet",
    "polygon_mumbai",
    "optimism_mainnet",
    "optimism_goerli",
    "gnosis_mainnet",
    "gnosis_chiado",
    "linea_goerli",
    "scroll_goerli",
    "neon_devnet",
    "mantle_testnet",
]


def get_web3(network: NETWORKS) -> Web3:
    try:
        endpoint = NETWORK_RPC_ENDPOINTS[network]
        return Web3(Web3.HTTPProvider(endpoint))
    except KeyError:
        raise ValueError(f"Unsupported network: {network}")

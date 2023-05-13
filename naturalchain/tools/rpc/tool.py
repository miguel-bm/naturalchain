import json
import re
from enum import Enum
from functools import lru_cache
from typing import Literal, Union

from decouple import config
from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from web3 import Web3

INFURA_API_KEY = config("INFURA_API_KEY")

NETWORK = Literal[
    "ethereum_mainnet",
    "near_mainnet",
    "avalanche_mainnet",
]


def camel_to_snake(string):
    # Insert an underscore before any capital letters and convert to lowercase
    snake_case = re.sub(r"(?<!^)(?=[A-Z])", "_", string).lower()
    return snake_case


class RPCTool(BaseTool):
    name = "RPC"
    description = "Useful for getting data with RPC"

    def _get_web3(self, network: str) -> Web3:
        if network == "ethereum_mainnet":
            rpc_endpoint = f"https://mainnet.infura.io/v3/{INFURA_API_KEY}"
        elif network == "near_mainnet":
            rpc_endpoint = f"https://near-mainnet.infura.io/v3/{INFURA_API_KEY}"
        elif network == "avalanche_mainnet":
            rpc_endpoint = f"https://avalanche-mainnet.infura.io/v3/{INFURA_API_KEY}"
        else:
            raise ValueError(f"Unsupported network: {network}")

        return Web3(Web3.HTTPProvider(rpc_endpoint))

    def _get_method(self, payload: dict) -> tuple[str, str]:
        # The payload method should be something like "eth_call" or "eth_getBalance"
        payload_method = payload["method"]

        # Split the method into the prefix and the method name
        split_method = re.split(r"[_\W]", payload_method)

        # Return the prefix and the method name in snake case
        return split_method[0], camel_to_snake(split_method[1])

    def _get_params(self, payload: dict) -> dict:
        return payload["params"]

    # def _make_eth_call(self, web3: Web3, payload: dict) -> str:
    #     params = self._get_params(payload)

    #     response = web3.eth.call(params[0])

    #     print(response)
    #     return response.hex()

    # def _make_generic_call(self, web3: Web3, payload: dict) -> str:
    #     method_1, method_2 = self._get_method(payload)
    #     params = self._get_params(payload)

    #     response = getattr(getattr(web3, method_1), method_2)(params[0])
    #     return response

    def _make_rpc_call(self, web3: Web3, payload: dict) -> str:
        method_1, method_2 = self._get_method(payload)
        params = self._get_params(payload)

        response = getattr(getattr(web3, method_1), method_2)(params[0])
        return response

    def _run(self, network: NETWORK, payload: Union[str, dict]) -> str:
        if isinstance(payload, str):
            payload: dict = json.loads(payload)
        # method = self._get_method(payload)

        web3 = self._get_web3(network)

        return self._make_rpc_call(web3, payload)

        # if method == ("eth", "call"):
        #     return self._make_eth_call(web3, payload)
        # else:
        #     return self._make_generic_call(web3, payload)

    async def _arun(self, address: str) -> str:
        raise NotImplementedError

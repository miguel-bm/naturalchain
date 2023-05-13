from typing import Type

from decouple import config
from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from web3 import Web3

INFURA_API_KEY = config("INFURA_API_KEY")
w3 = Web3(Web3.HTTPProvider(f"https://mainnet.infura.io/v3/{INFURA_API_KEY}"))


def is_contract(address):
    # Convert the address to a checksum address to ensure compatibility
    checksum_address = w3.toChecksumAddress(address)

    # Retrieve the bytecode of the contract
    bytecode = w3.eth.getCode(checksum_address)

    # Check if the contract has bytecode
    if bytecode:
        return True
    else:
        return False


def is_proxy(address):
    # Convert the address to a checksum address to ensure compatibility
    checksum_address = w3.toChecksumAddress(address)

    # Retrieve the bytecode of the contract
    storage_value = w3.eth.get_storage_at(
        checksum_address,
        "0x360894a13ba1a3210667c828492db98dca3e2076cc3735a920a3ca505d382bbc",
    ).hex()

    # Check if the contract has bytecode
    if storage_value == "0x" or int(storage_value, 16) == 0:
        return "0x"
    else:
        # Parse the storage value as an address (last 20 bytes)
        parsed_address = "0x" + storage_value[-40:]
        return parsed_address


class TrialToolSchema(BaseModel):
    address: str = Field(description="The address to the contract to be identified")


class IdentifyTool(BaseTool):
    name = "Identify contract"
    description = "Useful to identify a contract in the EVM blockchain. Return whether is a contract or not, and if it is a proxy, returns its implementation address"

    args_schema: Type[BaseModel] = TrialToolSchema

    def _run(self, address: str) -> object:
        isContract = is_contract(address)

        implementationAddress = "0x"
        if isContract:
            implementationAddress = is_proxy(address)
            if implementationAddress == "0x":
                return "The address is a contract"
            else:
                return f"The address is a proxy contract pointing to {implementationAddress}"
        else:
            return "The address is not a contract"

    async def _arun(self, address: str) -> str:
        raise NotImplementedError

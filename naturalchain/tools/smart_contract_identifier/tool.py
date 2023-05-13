from typing import Type

from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from web3 import Web3

from naturalchain.utils import NETWORKS, get_web3


def is_contract(w3: Web3, address: str):
    # Convert the address to a checksum address to ensure compatibility
    checksum_address = w3.toChecksumAddress(address)

    # Retrieve the bytecode of the contract
    bytecode = w3.eth.getCode(checksum_address)

    # Check if the contract has bytecode
    if bytecode:
        return True
    else:
        return False


def is_proxy(w3: Web3, address: str):
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


class IdentifyContractToolSchema(BaseModel):
    network: NETWORKS = Field(description="The network to use")
    address: str = Field(description="The address to the contract to be identified")


class IdentifyContractTool(BaseTool):
    name = "IdentifyContract"
    description = "Useful to identify a contract in the EVM blockchain. Given an address, returns whether it is a contract or not. If it is a proxy, returns its implementation address"

    args_schema: Type[BaseModel] = IdentifyContractToolSchema

    def _run(self, network: NETWORKS, address: str) -> object:
        web3 = get_web3(network)

        isContract = is_contract(web3, address)

        implementationAddress = "0x"
        if isContract:
            implementationAddress = is_proxy(web3, address)
            if implementationAddress == "0x":
                return "The address is a contract"
            else:
                return f"The address is a proxy contract pointing to {implementationAddress}"
        else:
            return "The address is not a contract"

    async def _arun(self, address: str) -> str:
        raise NotImplementedError

from typing import Type
import binascii

from decouple import config
from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from web3 import Web3

INFURA_API_KEY = config("INFURA_API_KEY")
w3 = Web3(Web3.HTTPProvider(f"https://sepolia.infura.io/v3/{INFURA_API_KEY}"))
PRIVATE_KEY = config("PRIVATE_KEY")


def signTransaction(destinationAddress, value, data):
    # Create a raw transaction dictionary
    sender_address = w3.eth.account.from_key(PRIVATE_KEY).address
    gas_price = int(int(w3.eth.gas_price) * 1.1)

    gas_estimate = w3.eth.estimateGas({
        'from': sender_address,
        'to': destinationAddress,
        'value':value,  # Amount to send in Wei
        'data': data
    })

    transaction = {
        'to': destinationAddress,
        'value':value,  # Amount to send in Wei
        'gas': gas_estimate,  # Gas limit for a standard Ether transfer
        'gasPrice':gas_price,
        'nonce': w3.eth.getTransactionCount(sender_address),  # Nonce of the sender's address
        'data': data
    }

    # Sign the transaction
    signed_transaction = w3.eth.account.sign_transaction(transaction, PRIVATE_KEY)

    # Send the signed transaction
    transaction_hash = w3.eth.send_raw_transaction(signed_transaction.rawTransaction)

    # Wait for the transaction to be mined
    transaction_receipt = w3.eth.wait_for_transaction_receipt(transaction_hash)

    return transaction_receipt

    

class SignToolSchema(BaseModel):
    smartContractAddress: str = Field(
        description="Smart contract address, can be the destination address if it's not a smart contract"
    )
    value: str = Field(
        description="Ether value of in weis"
    )
    data: str = Field(
        description="Data of the ethereum transaction"
    )


class SignTransactionTool(BaseTool):
    name = "Signer tool"
    description = "Useful to send transactions given a smart contract address, ether value and data. Return the receipt"

    args_schema: Type[BaseModel] = SignToolSchema

    def _run(self, smartContractAddress: str, value: str, data: str) -> str:
        checksum_address = w3.toChecksumAddress(smartContractAddress)
        transaction_receipt = signTransaction(checksum_address, int(value), data)

        # Check the transaction status
        return str(transaction_receipt)

    async def _arun(self, smartContractAddress: str, value: str, data: str) -> str:
        raise NotImplementedError

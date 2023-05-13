from typing import Type

from decouple import config
from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from web3 import Web3
from naturalchain.utils import NETWORKS, get_web3


def signTransaction(
    w3: Web3,
    deatination_address: str,
    value: int,
    data,
):
    # Create a raw transaction dictionary
    private_key = config("PRIVATE_KEY")

    sender_address = w3.eth.account.from_key(private_key).address
    gas_price = int(int(w3.eth.gas_price) * 1.1)

    gas_estimate = w3.eth.estimateGas(
        {
            "from": sender_address,
            "to": deatination_address,
            "value": value,  # Amount to send in Wei
            "data": data,
        }
    )

    transaction = {
        "to": deatination_address,
        "value": value,  # Amount to send in Wei
        "gas": gas_estimate,  # Gas limit for a standard Ether transfer
        "gasPrice": gas_price,
        "nonce": w3.eth.getTransactionCount(
            sender_address
        ),  # Nonce of the sender's address
        "data": data,
    }

    # Sign the transaction
    signed_transaction = w3.eth.account.sign_transaction(transaction, private_key)

    # Send the signed transaction
    transaction_hash = w3.eth.send_raw_transaction(signed_transaction.rawTransaction)

    # Wait for the transaction to be mined
    transaction_receipt = w3.eth.wait_for_transaction_receipt(transaction_hash)

    return transaction_receipt


class SignTransactionToolInput(BaseModel):
    smart_contract_address: str = Field(
        description="Smart contract address, can be the destination address if it's not a smart contract"
    )
    value: str = Field(description="Ether value of in weis")
    data: str = Field(description="Data of the ethereum transaction")
    network: NETWORKS = Field(
        description="The network to interact with the smart contract."
    )


class SignTransactionTool(BaseTool):
    name = "Signer tool"
    description = "Useful for sending transactions given a smart contract address, ether value, data and network to interact with. Return the receipt"

    args_schema: Type[BaseModel] = SignTransactionToolInput

    def _run(
        self,
        smart_contract_address: str,
        value: str,
        data: str,
        network: NETWORKS,
    ) -> str:
        w3 = get_web3(network)
        checksum_address = w3.toChecksumAddress(smart_contract_address)
        transaction_receipt = signTransaction(w3, checksum_address, int(value), data)

        # Check the transaction status
        return str(transaction_receipt)

    async def _arun(
        self,
        smartContractAddress: str,
        value: str,
        data: str,
        network: NETWORKS,
    ) -> str:
        raise NotImplementedError

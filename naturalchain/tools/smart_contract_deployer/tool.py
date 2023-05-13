from pathlib import Path
from typing import Optional, Type

from decouple import config
from langchain.callbacks.manager import CallbackManagerForToolRun
from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from web3.middleware.geth_poa import geth_poa_middleware

from naturalchain.utils import NETWORKS, get_web3


class SmartContractDeployerToolInput(BaseModel):
    path_to_bytecode: str = Field(
        description="The path to the text file containing the bytecode of the smart contract"
    )
    network: NETWORKS = Field(
        description="The network to deploy the smart contract to."
    )


class SmartContractDeployerTool(BaseTool):
    name = "SmartContractDeployer"
    description = "Useful for deploying EVM-compatible smart contracts given a path to a file containing the bytecode and the network to deploy to. Returns the address of the deployed contract."
    args_schema: Type[BaseModel] = SmartContractDeployerToolInput

    def _run(
        self,
        path_to_bytecode: str,
        network: NETWORKS,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        w3 = get_web3(network)
        # Load the bytecode as str
        with Path(path_to_bytecode).open("r") as f:
            bytecode = f.read()

        # Get the public address associated with the private key
        private_key = config("PRIVATE_KEY")
        public_address = w3.eth.account.privateKeyToAccount(private_key).address

        # Inject the PoA middleware to the w3 instance in case of a PoA network
        w3.middleware_onion.inject(geth_poa_middleware, layer=0)

        # Check if you have enough Ether
        balance = w3.eth.getBalance(public_address)
        if balance <= 0:
            raise ValueError(
                "Your account does not have enough balance to deploy a Smart Contract. Add some before proceeding."
            )

        # Estimate gas for deployment
        gas_estimate = w3.eth.estimateGas(
            {"from": public_address, "data": f"0x{bytecode}"}
        )

        # Get nonce
        nonce = w3.eth.getTransactionCount(public_address)
        # Get gas price
        gas_price = w3.eth.gasPrice

        # Prepare the transaction
        transaction = {
            "from": public_address,
            "gas": gas_estimate,
            "gasPrice": w3.eth.gasPrice,
            "data": f"0x{bytecode}",
            "nonce": nonce,
            "chainId": w3.eth.chainId,
        }

        # Sign the transaction
        signed_tx = w3.eth.account.signTransaction(transaction, private_key)

        # Send the transaction
        try:
            transaction_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
        except ValueError as e:
            required_token = gas_estimate * gas_price
            raise ValueError(
                f"{e}. This operation required token: {required_token / 1e18}"
            )

        # Wait for the transaction receipt
        transaction_receipt = w3.eth.waitForTransactionReceipt(transaction_hash)

        # Get the contract address
        contract_address: str = transaction_receipt["contractAddress"]

        return contract_address

    async def _arun(
        self,
        description: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        raise NotImplementedError("This tool does not support async mode.")


if __name__ == "__main__":
    tool = SmartContractDeployerTool()

    result = tool._run(
        path_to_bytecode="/Users/miguel/Developer/projects/naturalchain/smart_contracts/smart_contract_2023-05-13-11-09-42-bin",
        network="ethereum_sepolia",
    )

    print(result)

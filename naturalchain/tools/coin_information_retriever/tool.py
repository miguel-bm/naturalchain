import json
from typing import Optional

import requests
from decouple import config
from langchain.callbacks.manager import CallbackManagerForToolRun
from langchain.tools import BaseTool

from naturalchain.utils import CMC_NETWORK_NAMES, NETWORKS, get_web3
from pydantic import BaseModel, Field
from typing import Type

COIN_MARKET_CAP_API_KEY = config("COIN_MARKET_CAP_API_KEY")


class CoinInformationRetrieverToolInput(BaseModel):
    symbol: str = Field(description="Symbol of the coin in coinmarketcap.")
    network: Optional[NETWORKS] = Field(
        description="Optional, network of the coin.",
        default="ethereum_mainnet",
    )


class CoinInformationRetrieverTool(BaseTool):
    name = "TokenInformation"
    description = "Useful for retrieving current token information. Returns a json object with address, name, symbol, token_supply, price"
    args_schema: Type[BaseModel] = CoinInformationRetrieverToolInput

    @staticmethod
    def _get_coin_address(network: NETWORKS, symbol: str):
        url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/info"
        parameters = {"symbol": symbol}
        headers = {
            "Accepts": "application/json",
            "X-CMC_PRO_API_KEY": COIN_MARKET_CAP_API_KEY,
        }

        response = requests.get(url, headers=headers, params=parameters)
        data = json.loads(response.text)

        contract_addresses_list = data["data"][symbol]["contract_address"]

        for address_info in contract_addresses_list:
            if address_info["platform"]["name"] == CMC_NETWORK_NAMES[network]:
                address = address_info["contract_address"]
                web3 = get_web3(network)
                return web3.toChecksumAddress(address)

        return "No address found"

    @staticmethod
    def _get_coin_basic_info(symbol: str):
        url = "https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest"
        parameters = {"symbol": symbol}
        headers = {
            "Accepts": "application/json",
            "X-CMC_PRO_API_KEY": COIN_MARKET_CAP_API_KEY,
        }

        response = requests.get(url, headers=headers, params=parameters)
        data = json.loads(response.text)

        coin_data = data["data"][symbol][0]

        return {
            "name": coin_data["name"],
            "symbol": coin_data["symbol"],
            "total_supply": coin_data["total_supply"],
            "price": coin_data["quote"]["USD"]["price"],
        }

    @staticmethod
    def _get_coin_info(network: NETWORKS, symbol: str):
        if not symbol:
            return {"error": "No symbol provided."}
        try:
            address = CoinInformationRetrieverTool._get_coin_address(network, symbol)
            coin_info = CoinInformationRetrieverTool._get_coin_basic_info(symbol)
        except Exception as e:
            return {"error": "Invalid symbol."}
        coin_info["address"] = address
        return {
            "address": address,
            **coin_info,
        }

    def _run(
        self,
        symbol: str,
        network: NETWORKS = "ethereum_mainnet",
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        return json.dumps(self._get_coin_info(network, symbol))

    def _arun(
        self,
        network: NETWORKS,
        symbol: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        raise NotImplementedError

import json
import re
from typing import Optional, Union

from langchain.callbacks.manager import CallbackManagerForToolRun
from langchain.tools import BaseTool
from web3 import Web3

from naturalchain.utils import NETWORKS, camel_to_snake, get_web3


class RPCTool(BaseTool):
    name = "RPC"
    description = "Useful for getting data with RPC"

    def _get_method(self, payload: dict) -> tuple[str, str]:
        # The payload method should be something like "eth_call" or "eth_getBalance"
        payload_method = payload["method"]

        # Split the method into the prefix and the method name
        split_method = re.split(r"[_\W]", payload_method)

        # Return the prefix and the method name in snake case
        return split_method[0], camel_to_snake(split_method[1])

    def _get_params(self, payload: dict) -> dict:
        return payload["params"]

    def _make_rpc_call(self, web3: Web3, payload: dict) -> str:
        method_1, method_2 = self._get_method(payload)
        params = self._get_params(payload)

        response = getattr(getattr(web3, method_1), method_2)(params[0])
        return response

    def _run(
        self,
        network: NETWORKS,  # type: ignore
        payload: Union[str, dict],
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        if isinstance(payload, str):
            payload_dict: dict = json.loads(payload)
        else:
            payload_dict = payload

        web3 = get_web3(network)

        return self._make_rpc_call(web3, payload_dict)

    async def _arun(self, address: str) -> str:
        raise NotImplementedError

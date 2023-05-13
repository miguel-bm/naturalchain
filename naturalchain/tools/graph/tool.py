from typing import Type
import binascii

from decouple import config
from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from web3 import Web3
from naturalchain.utils import NETWORKS, get_web3
import requests
import json


def queryGraph(query: str, endpoint: str):
    #endpoint = 'https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v3'

    headers = {'Content-Type': 'application/json'}
    data = json.dumps({'query': query})

    response = requests.post(endpoint, headers=headers, data=data)

    return response


class UniswapGraphSquema(BaseModel):
    query: str = Field(
        description="Graph query to be executed"
    )
    endpoint: str = Field(
        description="Full subgraph endpoint to be called including the https:// prefix"
    )

class UniswapGraphTool(BaseTool):
    name = "Graph tool"
    description = "Useful for quering the graph, which provides usefull information about pools"

    args_schema: Type[BaseModel] = UniswapGraphSquema

    def _run(self, query: str, endpoint: str) -> str:
        response = queryGraph(query, endpoint)

        if response.status_code == 200:
           jsonResponse = response.json()
           if 'errors' in jsonResponse:
                return  jsonResponse['errors'][0]['message']
                #return  "The error of the last query was" + jsonResponse['errors'][0]['message'] + "\n Try to query properly the graph taking in account the graph schema"
           else:
              return jsonResponse
        else:
           return f'Request failed with status code {response.status_code}'



    async def _arun(self, query: str) -> str:
        raise NotImplementedError

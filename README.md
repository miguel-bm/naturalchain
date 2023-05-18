# NaturalChain: An AI Toolkit for Blockchain

![logo](./assets/logo.png)  

## Description  

NaturalChain is an AI toolkit that brings the power of Large Language Models (LLMs) like ChatGPT to the blockchain. NaturalChain aims to revolutionize blockchain interaction by allowing users to utilize natural language commands to perform complex tasks.

NaturalChain was originally developed for the ETHGlobal Lisbon 2023 hackathon by the team at Cenit Finance along with Jesús Ligero.

## Features

NaturalChain extends [LangChain](https://github.com/hwchase17/langchain). It uncludes tools includes that allow an AI agent to:

- Utilize the full JSON-RPC API from an EVM-compatible chain.
- Sign transactions
- Write and deploy smart contracts
- Query from APIs (The Graph, CoinMarketCap, etc.)

By default it uses ChatGPT 3.5, but you can hook it up to any LLM you wish.

## Prerequisites

This project uses Python 3.9, [Poetry](https://python-poetry.org/docs/), and [just](https://github.com/casey/just).



## Installation

Project installation:


```bash
git clone https://github.com/miguel-bm/naturalchain.git

cd naturalchain

poetry install

poetry shell
```



## Usage

In order to run the CLI interface:

```bash
naturalchain --help
```


In order to run the chat interface weapp

```bash
just run
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Acknowledgments

Special thanks to the ETHGlobal Lisbon Hackathon and its sponsors.

## Example prompts:

- Deploy Smart contracts
    - Create a nft smart contract with a preminted nft to the deployer address on sepolia network
    - Create a nft smart contract based on dnd on Sepolia
    - Deploy an nft contract on Sepolia, ask any questions about the process
    - Create an erc20 dnd oriented onSepolia, ask any questions about the process
        - Send a transaction to interact with this erc20 contract 0x7484e7449Ca8b3c9807E191b9A7E75319daa1Af4 to transfer 25 tokens to this address 0xf904C9Be6884263606BC9C41fb17b16D4c692C02 on Sepolia

- Querying subgraph
    - Can you provide me the top 10 pairs of uniswap?
    - Can you provide me the top 5 uniswap pairs that have DAI on it?
    - Show top pairs of balancer
    - Can you provide me the top 5 paris of uniswap and provide the reserved of USD of each one?

- Leverage the full JSON-rpc
    - Send 0.01 ether to this address 0xf904C9Be6884263606BC9C41fb17b16D4c692C02 on Sepolia
    - Get the account information of this address 0x2a3DD3EB832aF982ec71669E178424b10Dca2EDe on mainnet

    
# NaturalChain

## To-dos 
[x] Choose Mainnet, Testnet, Polygon... (@Alvaro)
[x] Full RPC tool (@Alvaro)
[x] List of cool test cases for our RPC agent (@Jesus)
[x] Tool for creating smart contracts (@Miguel)
[x] CLI for our agent 
[x] Tool for compiling smart contracts
[x] Tool for deploying smart contracts
[x] Add all networks we want to deploy to
[x] Coinmarketcap price tool
[] TheGraph Tool for their API
[] Complete README.md
[] Deploy on all the chains


## Ideas extra

- Usar la API de Etherscan para pedir ERC20 transfers, las transacciones que ha hecho una cuenta...
- Herramienta para AirStack


## Example prompts:


- Deploy Smart contracts
    - Create a nft smart contract with a preminted nft to the deployer address on sepolia network
    - Create a nft smart contract based on dnd on Sepolia


    - Deploy an nft contract on Sepolia, ask any questions about the process
    - Create an erc20 dnd oriented on Sepolia, ask any questions about the process
        - Send a transaction to interact with this erc20 contract 0x2d8De0cC5775aBB07a3994556Cfb15db08f7A17b to transfer 25 tokens to this address 0xf904C9Be6884263606BC9C41fb17b16D4c692C02 on Sepolia

- Querying subgraph
    - Can you provide me the top 10 pairs of uniswap?
    - Can you provide me the top 5 uniswap pairs that have DAI on it?
    - Show top pairs of balancer

- Leverage the full JSON-rpc
    - Send 0.01 ether to this address 0xf904C9Be6884263606BC9C41fb17b16D4c692C02 on Sepolia
    - Get the account information of this address 0x2a3DD3EB832aF982ec71669E178424b10Dca2EDe on mainnet

    
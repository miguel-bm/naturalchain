# Ideas

## RPC

- Get account information
    - Given an address
        - Nonce: eth_getTransactionCount
        - Bytecode: eth_getCode
        - Balance: eth_getBalance
    - Given address say wheather or not is a proxy;
        - eth_getStorageAt: `bytes32 internal constant _IMPLEMENTATION_SLOT = 0x360894a13ba1a3210667c828492db98dca3e2076cc3735a920a3ca505d382bbc;`   
    - GIven an address and a event (submitDeposit..), sum all the balances to get the total value birdged to that network
- Smart contract deployment:
    - ERC721 (NFT) : 
        - Make an nft contract, supply is limited to 1000 and can only be minted paying a 0.01 ethers. 
    - ERC20: 
        - Write and deploy a smart contract on ethereum sepolia testnet for an erc20 where supply is limited to 1 Billion. Implements permit functionality. There is a minter address that can mint tokens. Give me the deployed contrac address
    - Charity:
        - Create a smart contract that accepts donations into registered projects. Everyone can register a project. Every project registered will have an ID and an IPFS link to theis project metadata and a recipient address. Contract tracks the donated amount for every project. Withdraw method to retrieve the donated amount
    - Oracle: 

- Guess the contract?: Given an address, check the events --> get the transactions that go to them and try to guess the contract giving that information ( can check the signatures of data (check 4 byte directory api), or logs signatures aswell ( https://github.com/otterscan/topic0))


## Extra

- Graph
    - Query all token balance sof an account, later on we could use the coingecko api to know the USD total amount


- etherscan: 
    - https://docs.etherscan.io/api-endpoints/contracts
    - Given an address, see if it has bytecode ( check eth_getbytecode) and if it does, try to fetch the contract form etherescan. 
        - ABI: to interact with SC
        - Solidity file: To let understand GPT the functions
        - Afterward we could ask to interact with the smart contract, (or even hack it?), 
https://docs.etherscan.io/api-endpoints/contracts
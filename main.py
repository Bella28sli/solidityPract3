import configuration as cf
from web3 import Web3
from web3.middleware import geth_poa_middleware 
# импортим всякое
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545')) 
# наш блокчейн
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
# хз че это
contract = w3.eth.contract(address=cf.CONTRACT_ADDRESS, abi=cf.ABI)
# экземпляр контракта

accounts = w3.eth.accounts
for i in range(len(accounts)):
    print(f"Баланс {i+1} аккаунта: {w3.eth.get_balance(accounts[i])}")
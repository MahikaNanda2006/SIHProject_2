from web3 import Web3
from solcx import compile_standard, install_solc
import json

# 1️⃣ Install Solidity compiler
install_solc("0.8.20")

# 2️⃣ Connect to Ganache
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
chain_id = 5777
my_address = "0x44fb547C24E1042adf6B16Ad23F2361808116Bec"
private_key = "0x8f4925f2d0b28217229efba4820fa307f47c07bcc1f6c7b678da7632bf9eaadd"

# 3️⃣ Read Solidity contract
with open("SupplyChain.sol", "r") as file:
    supply_chain_source = file.read()

# 4️⃣ Compile contract
compiled_sol = compile_standard({
    "language": "Solidity",
    "sources": {"SupplyChain.sol": {"content": supply_chain_source}},
    "settings": {
        "outputSelection": {
            "*": {
                "*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]
            }
        }
    }
}, solc_version="0.8.20")

# 5️⃣ Save ABI
abi = compiled_sol["contracts"]["SupplyChain.sol"]["SupplyChain"]["abi"]
with open("contract_abi.json", "w") as file:
    json.dump(abi, file)

# 6️⃣ Get bytecode
bytecode = compiled_sol["contracts"]["SupplyChain.sol"]["SupplyChain"]["evm"]["bytecode"]["object"]

# 7️⃣ Create contract object
SupplyChain = w3.eth.contract(abi=abi, bytecode=bytecode)

# 8️⃣ Get nonce
nonce = w3.eth.get_transaction_count(my_address)

# 9️⃣ Build transaction (no constructor needed)
transaction = SupplyChain.constructor().build_transaction({
    "chainId": chain_id,
    "from": my_address,
    "nonce": nonce,
    "gas": 6721975,
    "gasPrice": w3.eth.gas_price
})

# 1️⃣0️⃣ Sign transaction
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)

# 1️⃣1️⃣ Send transaction
tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)

# 1️⃣2️⃣ Wait for receipt
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

# ✅ Print contract address
print(f"Contract deployed at address: {tx_receipt.contractAddress}")

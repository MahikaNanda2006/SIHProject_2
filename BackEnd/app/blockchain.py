from web3 import Web3
import json

# -----------------------------
# Connect to Ganache
# -----------------------------
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))

if not w3.isConnected():
    raise Exception("Cannot connect to Ganache. Make sure Ganache is running!")

# Use the first account by default
w3.eth.default_account = w3.eth.accounts[0]

# -----------------------------
# Load ABI and Contract Address
# -----------------------------
with open("blockchain/contract_abi.json") as f:
    abi = json.load(f)

with open("blockchain/contract_address.txt") as f:
    contract_address = f.read().strip()

contract = w3.eth.contract(address=contract_address, abi=abi)

# -----------------------------
# Blockchain Functions
# -----------------------------

def add_collection_event(collector, herb_name, date, location):
    """
    Adds a new collection event to the blockchain.
    Returns the transaction receipt.
    """
    try:
        tx_hash = contract.functions.addCollectionEvent(
            collector, herb_name, date, location
        ).transact()
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        return tx_receipt
    except Exception as e:
        print("Error adding collection event:", e)
        return None


def get_provenance(herb_name):
    """
    Retrieves all collection events for a given herb.
    Returns a list of events.
    """
    try:
        events = contract.functions.getProvenance(herb_name).call()
        return events
    except Exception as e:
        print("Error fetching provenance:", e)
        return []

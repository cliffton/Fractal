import requests

# Register Second Node
node = {
    "nodes": [],
    "new-node": "127.0.0.1:5001"
}

rep = requests.post("http://localhost:5000/nodes/register", json=node)

# Register First Node

node = {
    "nodes": [],
    "new-node": "127.0.0.1:5000"
}

rep = requests.post("http://localhost:5000/nodes/register", json=node)

# Send Transaction 1
t1 = {
    "nodes": [],
    "transaction": {
        "sender": "d4ee26eee15148ee92c6cd394edd974e",
        "recipient": "someone-other-address",
        "amount": 1
    }
}
rep = requests.post("http://localhost:5000/transactions/new", json=t1)

# Send Transaction 2
t2 = {
    "nodes": [],
    "transaction": {
        "sender": "d4ee26eee15148ee92c6cd394edd974e",
        "recipient": "someone-other-address",
        "amount": 2
    }
}
rep = requests.post("http://localhost:5000/transactions/new", json=t2)

# Mine Block 1
rep = requests.get("http://localhost:5000/mine")

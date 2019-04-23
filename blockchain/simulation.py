import random
import time
from uuid import uuid4

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
        "amount": 2,
        "uuid": str(uuid4())
    }
}
rep = requests.post("http://localhost:5000/transactions/new", json=t2)

# Mine Block 1
# rep = requests.get("http://localhost:5000/mine")

count = 2
while True:
    count += 1
    timeDelay = random.randrange(10, 20)
    time.sleep(timeDelay)
    recipients = ["Modi", "Rahul", "Kejriwal"]
    servers = ["5000", "5001", "5002", "5003"]
    t2 = {
        "nodes": [],
        "transaction": {
            "sender": str(uuid4()),
            "recipient": recipients[random.randrange(0, 3)],
            "amount": 1,
            "uuid": str(uuid4())
        }
    }
    try:
        rep = requests.post("http://localhost:" + servers[random.randrange(0, 4)] + "/transactions/new", json=t2)
    except Exception as e:
        print(str(e))

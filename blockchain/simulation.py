import random
import sys
import time
from uuid import uuid4
import logging
import requests

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# CANDIDATES = ["Narendra Modi", "Rahul Gandhi", "Arvind Kejriwal"]
CANDIDATES = ["Candidate 1", "Candidate 2", "Candidate 3"]
SERVERS = ["5000", "5001", "5002", "5003"]


def register_nodes():
    for server in SERVERS:
        try:
            logging.info("> Registering server: " + "127.0.0.1:" + server)
            node_url = "http://127.0.0.1:" + server + "/nodes/register"
            for s in SERVERS:
                data = {
                    "nodes": [],
                    "new-node": "127.0.0.1:" + s
                }
                requests.post(node_url, json=data)
        except Exception as e:
            logging.info(str(e))


def votes(max_count):
    count = 0
    while count < max_count:
        count += 1
        delay = random.randrange(1, 3)
        time.sleep(delay)
        candidate = CANDIDATES[random.randrange(0, 3)]
        t = {
            "nodes": [],
            "transaction": {
                "sender": str(uuid4()),
                "recipient": candidate,
                "amount": 1,
                "uuid": str(uuid4())
            }
        }
        try:
            server = SERVERS[random.randrange(0, 4)]
            logging.info("> Sending vote for " + candidate + " to server: " + server)
            requests.post("http://localhost:" + server + "/transactions/new", json=t)
        except Exception as e:
            logging.error(str(e))


def stop():
    try:
        for server in SERVERS:
            logging.info("> Stopping server: " + server)
            node_url = "http://127.0.0.1:" + server + "/stop"
            requests.get(node_url)
        requests.get("http://127.0.0.1:5000/mine")
    except Exception as e:
        logging.error(str(e))


def forks():
    try:
        for server in SERVERS:
            node_url = "http://127.0.0.1:" + server + "/nodes/forks"
            resp = requests.get(node_url)
            data = resp.json()
            logger.info("Number of discarded blocks:" + str(data))
    except Exception as e:
        logging.error(str(e))


def results():
    try:
        prev = None
        for server in SERVERS:

            result = {}
            for candidate in CANDIDATES:
                result.update({candidate: 0})
            node_url = "http://127.0.0.1:" + server + "/chain"
            resp = requests.get(node_url)
            chain = resp.json()["chain"]
            for block in chain:
                for txt in block["transactions"]:
                    result[txt["recipient"]] += 1
            prev = result
            # logging.info("Server:" + server + " result: " + str(result))
        logging.info("Server result: " + str(prev))
    except Exception as e:
        logging.error(str(e))


def run(num_votes):
    register_nodes()
    votes(num_votes)
    stop()
    results()
    forks()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python simulation.py <number-of-votes>")
    run(int(sys.argv[1]))

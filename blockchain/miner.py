import hashlib
import json
import random
import time
import logging

logger = logging.getLogger(__name__)


def output_reset(uri):
    f = open(uri + "mine-out.out", "w")
    f.close()


# @staticmethod
def mine(node):
    # f = open(node.node_identifier + "mine-out.out", "a")
    # f.write("new mining...\n")
    # f.close()

    logger.error("minning - " + node.node_identifier)
    current = node.blockchain.last_block
    proof = proof_of_work(current['proof'], node)
    if proof == None:
        # f = open(node.node_identifier + "mine-out.out", "a")
        # f.write("not found\n")
        # f.close()
        logger.error("minning - " + node.node_identifier + "-- not found")
        mine(node)
    else:
        t = time.time()

        # f = open(node.node_identifier + "mine-out.out", "a")
        # f.write("found " + str(t) + str(proof) + "\n")
        # f.close()
        logger.error("minning - " + node.node_identifier + "-- found " + str(t) + " = " + str(proof))

        node.blockchain.new_block(proof, current['proof'])
        mine(node)


def hash(block):
    """
        Creates a SHA-256 hash of a Block
        :param block: <dict> Block
        :return: <str>
    """
    # We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
    block_string = json.dumps(block, sort_keys=True).encode()
    return hashlib.sha256(block_string).hexdigest()


# @staticmethod
def proof_of_work(last_proof, node):
    """
        Simple Proof of Work Algorithm:
         - Find a number p' such that hash(pp') contains leading 4 zeroes, where p is the previous p'
         - p is the previous proof, and p' is the new proof
        :param last_proof: <int>
        :param node : Node
        :return: <int>
    """
    proof = 0

    while valid_proof(last_proof, proof) is False:
        if last_proof != node.get_last_hash():
            return
        proof += 1
    timeDelay = random.randrange(0, 4)
    time.sleep(timeDelay)
    return proof


# @staticmethod
def valid_proof(last_proof, proof):
    """
        Validates the Proof: Does hash(last_proof, proof) contain 4 leading zeroes?
        :param last_proof: <int> Previous Proof
        :param proof: <int> Current Proof
        :return: <bool> True if correct, False if not.
    """
    guess = f'{last_proof}{proof}'.encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
    nouce = "0000"
    return guess_hash[:len(nouce)] == nouce

# import requests
#
#
# def get_network(node_url):
#     rep = requests.get("http://localhost:5000/nodes/all")
#     resp = rep.json()
#     nodes = resp.get("nodes")
#     nodes.append(node_url)
#     return nodes
#
#
# def mine():
#     while True:
#
#
# def main(node_url):
#     nodes = get_network(node_url)
#
#
# if __name__ == "__main__":
#     node_url = "http://localhost:5000/nodes/all"
#     main(node_url)

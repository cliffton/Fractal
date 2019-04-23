"""
CSCI-652 Project
@author Manpreet Kaur (mk3646)
@author Cliffton Fernandes (cf6715)
"""
import hashlib
import json
from time import time
import logging
import requests

logger = logging.getLogger(__name__)


class Blockchain:
    """
    This class represents in the blockchain.
    It provides methods to add, check and varify the
    blockchain.
    """

    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.current_transaction_uuids = []
        self.nodes = set()

        # Create genesis block
        self.new_block(previous_hash=1, proof=1)

    def valid_chain(self, chain):
        """
        Checks if the chain is valid by
        iterating through the chain and checking the
        hash of each block matching the last block.
        :param chain: block chain
        :return: True/False
        """

        logger.error("Checking validity.")

        previous_block = chain[0]
        block_index = 1

        while block_index < len(chain):
            current_block = chain[block_index]
            if current_block['previous_hash'] != Blockchain.hash(previous_block):
                return False

            if not Blockchain.valid_proof(previous_block['proof'], current_block['proof']):
                return False

            previous_block = current_block
            block_index += 1

        return True

    def resolve_conflicts(self):
        """
        Resolves conflicts if one chain
        is longer than other chain
        in different nodes.
        :return: True/False
        """
        logger.error("Resolving Issues")
        new_chain = None
        max_length = len(self.chain)

        for n in self.nodes:
            response = requests.get("http://" + n + "/chain")

            if response.status_code == 200:
                chain = response.json()['chain']
                length = len(chain)

                if length >= max_length and Blockchain.valid_chain(chain):
                    max_length = length
                    new_chain = chain

        if new_chain:
            logger.info("Replacing new chain")
            self.chain = new_chain
            return True
        return False

    def new_block(self, proof, previous_hash=None):
        """
        Adds a new block to the blockchain
        :param proof:
        :param previous_hash:
        :return:
        """
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1])
        }

        self.current_transactions = []
        self.current_transaction_uuids = []
        self.chain.append(block)
        return block

    def new_transaction(self, sender, recipient, amount, uuid):
        """
            Creates new transactions in the system.
        """
        self.current_transaction_uuids.append(uuid)
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        })
        return self.last_block['index'] + 1

    @property
    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def hash(block):
        """
        Given a block generates the sha256 hash
        of the block.
        :param block: block
        :return:
        """
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @staticmethod
    def proof_of_work(last_proof, node):
        """
        The proof of work algorithm
        Given the proof of the last block it
        tries to find the proof of the next block.
        :param last_proof: proof of last block
        :param node: node
        :return: proof (int)
        """
        proof = 0
        while True:
            if node.blockchain.valid_proof(last_proof, proof):
                return proof
            current_proof = node.get_last_hash()
            if last_proof != current_proof:
                return
            proof += 1

    @staticmethod
    def valid_proof(previous_proof, proof):
        """
        Checks if hashing the last hash and the currect found hash
        returns a new hash with the last characters as zero.
        Basically varifies the nounce of the hash.
        :param previous_proof: previous proof
        :param proof: currect proof to varify
        :return: Boolean (True/False)
        """
        nouce = "000000"
        _tmp = f'{previous_proof}{proof}'.encode()
        new_hash = hashlib.sha256(_tmp).hexdigest()
        if new_hash[:len(nouce)] == nouce:
            return True
        return False

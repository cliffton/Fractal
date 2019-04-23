"""
CSCI-652 Project
@author Manpreet Kaur (mk3646)
@author Cliffton Fernandes (cf6715)
"""
from threading import Thread
from uuid import uuid4
from multiprocessing.dummy import Pool
from miner import mine
from blockchain import Blockchain
from flask import Flask
import requests
import logging

logger = logging.getLogger(__name__)

pool = Pool(10)


class Node(Flask):
    """
    Node class represents each node in the network
    The node is responsible for registering new nodes, accepting transactions
    mining blocks and broadcasting the transactions and blocks to
    the rest of the network.
    """

    def __init__(self, *args, **kwargs):
        self.node_identifier = str(uuid4()).replace('-', '')
        self.blockchain = Blockchain()
        self.network = set()
        self.ip = None
        self.port = None
        self.uri = None
        self.stop_simulation = False
        # Miner.mine(self)
        # Miner.output_reset(self.node_identifier)
        # pool.apply_async(Miner.mine, [self])
        t = Thread(target=mine, args=(self,))
        t.start()
        super().__init__(*args, **kwargs)

    def get_last_hash(self):
        """
        Returns the hash of the last block
        :return: hash (str)
        """
        return self.blockchain.last_block['proof']

    def set_uri(self, ip, port):
        """
        Given IP and port number
        sets the URI of the node
        :param ip: IP address
        :param port: Port number
        :return: None
        """
        self.ip = ip
        self.port = port
        self.uri = ip + ":" + port

    def register_node(self, n, values):
        """
        Given the node to register with
        and the details of the new node
        sends a request to the node.
        It is done asynchronously.
        :param n: Node to register with
        :param values: Details of node
        :return: None
        """
        try:
            node_url = "http://" + n + "/nodes/register"
            values["nodes"].append(self.uri)
            pool.apply_async(requests.post, [node_url],
                             kwds={"json": values})
        except Exception as e:
            logger.error(str(e))

    def send_transaction(self, n, values):
        """
            Given the node to send the transaction to
            and the details of the new transaction
            sends a request to the node.
            It is done asynchronously.
            :param n: Node to send transaction to
            :param values: Details of node
            :return: None
        """
        try:
            node_url = "http://" + n + "/transactions/new"
            values["nodes"].append(self.uri)
            # pool.apply_async(requests.post, [node_url],
            #                  kwds={"json": values})
            requests.post(node_url, json=values)
        except Exception as e:
            logger.error(str(e))

    def send_block_all(self, block):

        for n in self.network:
            values = {"nodes": [self.uri], "block": block}
            node.send_block(n, values)
        # self.blockchain.resolve_conflicts()

    def send_block(self, n, values):
        """
            Given the node to send the block to
            and the details of the new block
            sends a request to the node.
            It is done asynchronously.
            :param n: Node to send block to
            :param values: Details of block
            :return: None
        """
        try:
            node_url = "http://" + n + "/block/new"
            values["nodes"].append(self.uri)
            pool.apply_async(requests.post, [node_url],
                             kwds={"json": values})
        except Exception as e:
            logger.error(str(e))

    def __eq__(self, other):
        return self.node_identifier == other.node_identifier


node = Node(__name__)

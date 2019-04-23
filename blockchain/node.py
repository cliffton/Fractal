import json
import sys
from threading import Thread
from uuid import uuid4
from multiprocessing.dummy import Pool

import requests

from blockchain import Blockchain
from flask import Flask, jsonify, request

from miner import mine

pool = Pool(10)


class Node(Flask):

    def __init__(self, *args, **kwargs):
        self.node_identifier = str(uuid4()).replace('-', '')
        self.blockchain = Blockchain()
        self.network = set()
        self.ip = None
        self.port = None
        self.uri = None
        # Miner.mine(self)
        # Miner.output_reset(self.node_identifier)
        # pool.apply_async(Miner.mine, [self])
        t = Thread(target=mine, args=(self,))
        t.start()
        super().__init__(*args, **kwargs)

    def get_last_hash(self):
        return self.blockchain.last_block['proof']

    def set_uri(self, ip, port):
        self.ip = ip
        self.port = port
        self.uri = ip + ":" + port

    def register_node(self, n, values):
        node_url = "http://" + n + "/nodes/register"
        values["nodes"].append(self.uri)
        try:
            pool.apply_async(requests.post, [node_url],
                             kwds={"json": values})
        except Exception as e:
            print(str(e))

    def send_transaction(self, n, values):
        node_url = "http://" + n + "/transactions/new"
        values["nodes"].append(self.uri)
        try:
            # pool.apply_async(requests.post, [node_url],
            #                  kwds={"json": values})
            requests.post(node_url, json=values)
        except Exception as e:
            print(str(e))

    def send_block_all(self, block):
        for n in self.network:
            values = {"nodes": [self.uri], "block": block}
            node.send_block(n, values)
        self.blockchain.resolve_conflicts()

    def send_block(self, n, values):
        node_url = "http://" + n + "/block/new"
        values["nodes"].append(self.uri)
        try:
            pool.apply_async(requests.post, [node_url],
                             kwds={"json": values})
        except Exception as e:
            print(str(e))

    def __eq__(self, other):
        return self.node_identifier == other.node_identifier


node = Node(__name__)

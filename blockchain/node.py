import json
import sys
from uuid import uuid4
from multiprocessing.dummy import Pool

import requests

from blockchain import Blockchain
from flask import Flask, jsonify, request

pool = Pool(10)


class Node(Flask):

    def __init__(self, *args, **kwargs):
        self.node_identifier = str(uuid4()).replace('-', '')
        self.blockchain = Blockchain()
        self.network = set()
        self.ip = None
        self.port = None
        self.uri = None
        super().__init__(*args, **kwargs)

    def set_uri(self, ip, port):
        self.ip = ip
        self.port = port
        self.uri = ip + ":" + port

    def __eq__(self, other):
        return self.node_identifier == other.node_identifier

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

    def send_block(self, n, values):
        node_url = "http://" + n + "/block/new"
        values["nodes"].append(self.uri)
        try:
            pool.apply_async(requests.post, [node_url],
                             kwds={"json": values})
        except Exception as e:
            print(str(e))

    def send_block_all(self, block):
        for n in self.network:
            values = {"nodes": [self.uri], "block": block}
            node.send_block(n, values)
        self.blockchain.resolve_conflicts()


node = Node(__name__)

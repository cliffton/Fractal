import json
import sys
from uuid import uuid4

import requests

from blockchain import Blockchain
from flask import Flask, jsonify, request


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
            # req = requests.post(node_url, data=json.dumps(values))
            req = requests.post(node_url, json=values)
            print(req)
        except Exception as e:
            print("error")


node = Node(__name__)


def register_nodes():
    values = request.get_json()

    nodes = values.get('nodes')
    new_node = values.get('new-node')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for n in node.network:
        if n not in nodes:
            node.register_node(n, values)

    node.network.add(new_node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(node.network),
    }
    return jsonify(response), 201


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage")
        sys.exit()

    ip = sys.argv[1]
    port = sys.argv[2]
    node.add_url_rule('/nodes/register', None, register_nodes, methods=['POST'])
    node.set_uri(ip, port)
    node.run(host="0.0.0.0", port=port)

"""
CSCI-652 Project
@author Manpreet Kaur (mk3646)
@author Cliffton Fernandes (cf6715)
"""
from flask import request, jsonify

from node import *


def register_nodes():
    """
    POST API that registers new nodes.
    :return: Response
    """
    values = request.get_json()

    nodes = values.get('nodes')
    new_node = values.get('new-node')
    if new_node != node.uri:
        node.network.add(new_node)
        node.blockchain.nodes.add(new_node)

    for n in node.network:
        if n not in nodes:
            node.register_node(n, values)

    response = {
        'message': 'Node Added',
        'nodes': list(node.network),
    }
    return jsonify(response), 201


def get_nodes():
    """
    GET API that returns list of nodes.
    :return: Response
    """
    response = {
        'nodes': list(node.network),
    }
    return jsonify(response), 200


def get_transactions():
    """
    GET API that returns list of transaction.
    :return: Response
    """
    response = {
        'transaction': list(node.blockchain.current_transactions),
    }
    return jsonify(response), 200


def new_transactions():
    """
    POST API that adds transaction to the node.
    :return: Response
    """
    values = request.get_json()
    transaction = values.get("transaction")
    nodes = values.get('nodes')

    if transaction["uuid"] not in node.blockchain.current_transaction_uuids:
        index = node.blockchain.new_transaction(transaction['sender'], transaction['recipient'], transaction['amount'],
                                                transaction['uuid'])
        for n in node.network:
            if n not in nodes:
                node.send_transaction(n, values)

        response = {'message': 'Transaction recorded.'}
    else:
        response = {'message': 'Transaction already recorded.'}

    return jsonify(response), 201


def receive_block():
    """
    POST API that registers block.
    :return: Response
    """
    values = request.get_json()
    nodes = values.get("nodes")
    block = values.get("block")

    if block["proof"] not in [b["proof"] for b in node.blockchain.chain]:
        node.blockchain.current_transactions = []
        node.blockchain.current_transaction_uuids = []
        node.blockchain.chain.append(block)
        for n in node.network:
            if n not in nodes:
                node.send_block(n, values)
        # node.blockchain.resolve_conflicts()
    response = {'message': 'Block received'}

    return jsonify(response), 200


def mine():
    """
    GET API that mines the block.
    :return: Response
    """
    last_block = node.blockchain.last_block
    last_proof = last_block['proof']
    proof = node.blockchain.proof_of_work(last_proof, node)

    previous_hash = node.blockchain.hash(last_block)
    block = node.blockchain.new_block(proof, previous_hash)
    node.send_block_all(block)
    response = {
        'message': "Block found",
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }

    return jsonify(response), 200


def full_chain():
    """
    GET API that returns the entire block chain.
    :return: Response
    """
    # if not node.blockchain.valid_chain(node.blockchain.chain):
    #     node.blockchain.resolve_conflicts()
    response = {
        'chain': node.blockchain.chain
    }
    return jsonify(response), 200


def resolve():
    """
    GET API that resolves conflicts in the blockchain.
    :return: Response
    """
    node.blockchain.resolve_conflicts()

    response = {
        'chain': node.blockchain.chain
    }

    return jsonify(response), 200


def stop_simulation():
    """
    GET API that stops the mining.
    :return: Response
    """
    node.stop_simulation = True
    response = {"done": "done"}
    return jsonify(response), 200

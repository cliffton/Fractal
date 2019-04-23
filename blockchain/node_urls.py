"""
CSCI-652 Project
@author Manpreet Kaur (mk3646)
@author Cliffton Fernandes (cf6715)
"""
from flask import request, jsonify

from node import *


def register_nodes():
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
    response = {
        'nodes': list(node.network),
    }
    return jsonify(response), 200


def get_transactions():
    response = {
        'transaction': list(node.blockchain.current_transactions),
    }
    return jsonify(response), 200


def new_transactions():
    values = request.get_json()
    transaction = values.get("transaction")
    nodes = values.get('nodes')

    # Check that the required fields are in the POST'ed data
    required = ['sender', 'recipient', 'amount']
    if not all(k in transaction for k in required):
        return 'Missing values', 400

    # Create a new Transaction
    if transaction["uuid"] not in node.blockchain.current_transaction_uuids:
        index = node.blockchain.new_transaction(transaction['sender'], transaction['recipient'], transaction['amount'],
                                                transaction['uuid'])
        for n in node.network:
            if n not in nodes:
                node.send_transaction(n, values)

        response = {'message': f'Transaction will be added to Block {index}'}
    else:
        response = {}

    return jsonify(response), 201


def receive_block():
    values = request.get_json()
    nodes = values.get("nodes")
    block = values.get("block")

    if block not in node.blockchain.chain:
        node.blockchain.current_transactions = []
        node.blockchain.chain.append(block)
        for n in node.network:
            if n not in nodes:
                node.send_block(n, values)
        # node.blockchain.resolve_conflicts()
    response = {'message': f'Transaction will be added to Block'}

    return jsonify(response), 200


def mine():
    # We run the proof of work algorithm to get the next proof...
    last_block = node.blockchain.last_block
    last_proof = last_block['proof']
    proof = node.blockchain.proof_of_work(last_proof)

    # We must receive a reward for finding the proof.
    # The sender is "0" to signify that this node has mined a new coin.
    # node.blockchain.new_transaction(
    #     uuid=uuid4(),
    #     sender="0",
    #     recipient=node.node_identifier,
    #     amount=1,
    # )

    # Forge the new Block by adding it to the chain
    previous_hash = node.blockchain.hash(last_block)
    block = node.blockchain.new_block(proof, previous_hash)
    node.send_block_all(block)
    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }

    return jsonify(response), 200


def full_chain():
    # if not node.blockchain.valid_chain(node.blockchain.chain):
    #     node.blockchain.resolve_conflicts()
    response = {
        'chain': node.blockchain.chain,
        'length': len(node.blockchain.chain)
    }
    return jsonify(response), 200


def consensus():
    replaced = node.blockchain.resolve_conflicts()

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': node.blockchain.chain
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': node.blockchain.chain
        }

    return jsonify(response), 200


def stop_simulation():
    node.stop_simulation = True
    response = {"done": "done"}
    return jsonify(response), 200

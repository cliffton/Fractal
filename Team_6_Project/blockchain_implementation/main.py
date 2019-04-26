"""
CSCI-652 Project
@author Manpreet Kaur (mk3646)
@author Cliffton Fernandes (cf6715)
"""

import sys

from node_urls import *


def run(ip, port):
    """
    Main method
    Registers the urls.
    Registers the node with the network.
    Runs the server.
    :param ip: IP Addr
    :param port: port number
    :return: None
    """
    node.add_url_rule('/nodes/register', None, register_nodes, methods=['POST'])
    node.add_url_rule('/nodes/all', None, get_nodes, methods=['GET'])
    node.add_url_rule('/transactions/new', None, new_transactions, methods=['POST'])
    node.add_url_rule('/transactions/all', None, get_transactions, methods=['GET'])
    node.add_url_rule('/block/new', None, receive_block, methods=['POST'])
    node.add_url_rule('/mine', None, mine, methods=['GET'])
    node.add_url_rule('/chain', None, full_chain, methods=['GET'])
    node.add_url_rule('/nodes/resolve', None, resolve, methods=['GET'])
    node.add_url_rule('/nodes/forks', None, get_forks, methods=['GET'])
    node.add_url_rule('/stop', None, stop_simulation, methods=['GET'])
    node.set_uri(ip, port)

    # Registering with the network.
    register_node = node.ip + ":" + str(int(node.port) - 1)
    data = {"nodes": [], "new-node": node.uri}
    logger.error(register_node)
    logger.error(data)
    if int(node.port) > 5000:
        node.network.add(register_node)
        node.register_node(register_node, data)

    # Run the server
    node.run(host="0.0.0.0", port=port)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python main.py <IP-ADDRESS> <PORT>")
        sys.exit()

    ip = sys.argv[1]
    port = sys.argv[2]
    run(ip, port)

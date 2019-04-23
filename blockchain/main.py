from node_urls import *


def run(ip, port):
    node.add_url_rule('/nodes/register', None, register_nodes, methods=['POST'])
    node.add_url_rule('/nodes/all', None, get_nodes, methods=['GET'])
    node.add_url_rule('/transactions/new', None, new_transactions, methods=['POST'])
    node.add_url_rule('/transactions/all', None, get_transactions, methods=['GET'])
    node.add_url_rule('/block/new', None, receive_block, methods=['POST'])
    node.add_url_rule('/mine', None, mine, methods=['GET'])
    node.add_url_rule('/chain', None, full_chain, methods=['GET'])
    node.set_uri(ip, port)
    register_node = node.ip + ":" + str(int(node.port) - 1)
    data = {"nodes": [], "new-node": node.uri}
    logger.error(register_node)
    logger.error(data)
    if int(node.port) > 5000:
        node.network.add(register_node)
        node.register_node(register_node, data)
    node.run(host="0.0.0.0", port=port)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage")
        sys.exit()

    ip = sys.argv[1]
    port = sys.argv[2]
    run(ip, port)

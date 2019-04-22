from node_urls import *

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage")
        sys.exit()

    ip = sys.argv[1]
    port = sys.argv[2]
    node.add_url_rule('/nodes/register', None, register_nodes, methods=['POST'])
    node.add_url_rule('/nodes/all', None, get_nodes, methods=['GET'])
    node.add_url_rule('/transactions/new', None, new_transactions, methods=['POST'])
    node.add_url_rule('/transactions/all', None, get_transactions, methods=['GET'])
    node.add_url_rule('/block/new', None, receive_block, methods=['POST'])
    node.add_url_rule('/mine', None, mine, methods=['GET'])
    node.add_url_rule('/chain', None, full_chain, methods=['GET'])
    node.set_uri(ip, port)
    node.run(host="0.0.0.0", port=port)

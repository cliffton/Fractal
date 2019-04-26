"""
CSCI-652 Project
@author Manpreet Kaur (mk3646)
@author Cliffton Fernandes (cf6715)
"""

import time
import logging

logger = logging.getLogger(__name__)


def mine(node):
    """
    The method that mines the block
    for a node
    Runs in a thread
    :param node:
    :return:
    """
    if node.stop_simulation:
        return
    logger.error("Mining .... " + node.node_identifier)
    current = node.blockchain.last_block
    proof = node.blockchain.proof_of_work(node.get_last_hash(), node)
    if proof is None:
        logger.error("Block for - " + node.node_identifier + "- not found !")
        mine(node)
    else:
        t = time.time()
        logger.error("Block for - " + node.node_identifier + "-- found " + str(t) + " hash:= " + str(proof))
        node.blockchain.new_block(proof, current['proof'])
        node.send_block_all(node.blockchain.last_block)
        mine(node)

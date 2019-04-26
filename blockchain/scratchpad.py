import time
import hashlib

RUN = True
import matplotlib

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

import numpy as np
import pandas as pd


def valid_proof(last_proof, proof):
    guess = f'{last_proof}{proof}'.encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
    nouce = "0000000"  # 7
    return guess_hash[:len(nouce)] == nouce


def proof_of_work(last_proof, t_end):
    global RUN
    proof = 0
    while (valid_proof(last_proof, proof) is False) and time.time() < t_end:
        proof += 1
    return proof


def run():
    blocks = []
    t_end = time.time() + 60 * 5
    current = 1
    while time.time() < t_end:
        current = proof_of_work(current, t_end)
        blocks.append(current)
    print(len(blocks) / 60.0)


def draw():
    df = pd.DataFrame({'x': range(1, 11), 'y1': np.random.randn(10), 'y2': np.random.randn(10) + range(1, 11),
                       'y3': np.random.randn(10) + range(11, 21)})

    x = [12.116, 0.833, 0.033, 0.0166, 0.0166]
    # multiple line plot
    plt.plot(x, [1262, 64, 2, 2, 0], marker='o', markerfacecolor='blue', markersize=12, color='skyblue', linewidth=4,
             label="node1")
    plt.plot(x, [1116, 86, 3, 4, 0], marker='o', markerfacecolor='red', markersize=12, color='red', linewidth=4,
             label="node2")
    plt.plot(x, [1261, 93, 5, 2, 0], marker='o', markerfacecolor='brown', markersize=12, color='brown', linewidth=4,
             label="node3")
    plt.plot(x, [1250, 73, 6, 4, 0], marker='o', markerfacecolor='green', markersize=12, color='green', linewidth=4,
             label="node4")
    plt.xlabel("Blocks/sec")
    plt.ylabel("Number of discarded blocks")

    # plt.plot('x', 'y2', marker='', color='olive', linewidth=2)
    # plt.plot('x', 'y3', marker='', color='olive', linewidth=2, linestyle='dashed', label="toto")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    # draw()
    run()

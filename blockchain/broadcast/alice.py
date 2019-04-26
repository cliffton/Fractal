from pyp2p.net import *
import time

# Setup Alice's p2p node.
alice = Net(passive_bind="127.0.0.1", passive_port=44444, debug=1,
            servers=[{'addr': '127.0.0.1', 'port': '8000'}])
alice.start()
alice.bootstrap()
alice.advertise()

# Event loop.
while 1:
    print("alice")
    for con in alice:
        for reply in con:
            print(reply)

    time.sleep(1)

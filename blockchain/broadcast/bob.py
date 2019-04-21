from pyp2p.net import *

# Setup Bob's p2p node.
bob = Net(passive_bind="127.0.0.1", passive_port=44445, debug=1,
          servers=[{'addr': '127.0.0.1', 'port': '8000'}])
bob.start()
bob.bootstrap()
bob.advertise()

# Event loop.
while 1:
    print("bob")
    for con in bob:
        con.send_line("test")

    time.sleep(1)

from twisted.internet import reactor
from twisted.internet.protocol import Factory
from pyp2p.rendezvous_server import RendezvousFactory

factory = RendezvousFactory()
reactor.listenTCP(8000, factory, interface="0.0.0.0")
reactor.run()
from app.lib.base.provider import Provider
from app import create_app
from twisted.internet import reactor
from twisted.names.dns import DNSDatagramProtocol
from twisted.names import client
from app.lib.daemon.server.resolver import DatabaseDNSResolver
from app.lib.daemon.server.factory import DatabaseDNSFactory


class SnitchDaemon:
    def __init__(self, host, port, forwarding_enabled, forwarders):
        self.__host = host
        self.__port = port
        self.__forwarding_enabled = True if forwarding_enabled > 0 else False
        self.__forwarders = forwarders

    def start(self):
        clients = [DatabaseDNSResolver(create_app(), Provider().dns_manager())]
        if self.__forwarding_enabled and len(self.__forwarders) > 0:
            clients.append(client.Resolver(servers=self.__forwarders))

        factory = DatabaseDNSFactory(clients=clients)

        reactor.listenUDP(self.__port, DNSDatagramProtocol(factory), interface=self.__host)
        reactor.listenTCP(self.__port, factory, interface=self.__host)
        reactor.run()

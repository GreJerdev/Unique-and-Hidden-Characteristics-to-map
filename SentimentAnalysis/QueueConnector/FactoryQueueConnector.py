from bs4 import BeautifulSoup
from TCPQueueConnector import TCPQueueConnectorClient
from TCPQueueConnector import TCPQueueConnectorServer

import inspect

def GetQueueConnectorClient(configXML, logWriter = None):
    config = type('config', (object,), {})
    config.servers = []
    XML = configXML.managementunit.tcpqueue
    print XML.find_all('server')
    for serverXML in XML.find_all('server'):
        server = type('config', (object,), {})
        server.ip = serverXML.ip.string
        server.port = int(serverXML.port.string)
        server.maxNumberOfMsg = int(serverXML.maxnumberofmsg.string)
        config.servers.append(server)
    return TCPQueueConnectorClient(config, logWriter)


def GetQueueConnectorServer(configXML,processMsgFunction, logWriter = None):
    config = type('config', (object,), {})
    config.port = int(configXML.sentimentprocessuint.queue.port.string)
    return TCPQueueConnectorServer(processMsgFunction, config, logWriter)



from QueueConnector import FactoryQueueConnector
from configurationLoader import GetConfiguraton
configXml = GetConfiguraton(None)


def PrintData(msg):
    print len(msg)
    return "data processed"

Server = FactoryQueueConnector.GetQueueConnectorServer(configXml, PrintData,logWriter=None)

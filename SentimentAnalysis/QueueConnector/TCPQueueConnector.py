from twisted.internet import protocol, reactor, endpoints
from twisted.internet.protocol import Protocol
from twisted.internet.endpoints import TCP4ClientEndpoint, connectProtocol
from twisted.protocols import basic
from threading import Thread
from threading import Lock
import time
import Queue

from BaseQueueConnector import BaseQueueConnector

wiatTimeInsecs = 0.05
lock = Lock()
class TCPClient(basic.Int32StringReceiver):
        def __init__(self,tcpManager,ip,inQueue, outQueue, maxnumberofmsg):
            self.inQueue = inQueue
            self.outQueue = outQueue
            self.maxNumberOfMsgs = maxnumberofmsg    
            self.sentMsg = 0
            self.tcpManager = tcpManager
            self.ip = ip
            
            Thread(target=self.__sendDataFromQueue, args=()).start()

        def __sendDataFromQueue(self):
            while True:
                lock.acquire()    
                try:        
                    if not self.outQueue.empty() and self.maxNumberOfMsgs > self.sentMsg:
                        message = self.outQueue.get()
                        #print('get message %s from out queue and sending it. message len is %i' % (message,len(message),))
                        self.sendMessage(message)
                        self.sentMsg = self.sentMsg + 1
                    else:
                        if self.maxNumberOfMsgs <= self.sentMsg:
                            #print self.ip, '_______sentMsg___',self.sentMsg
                            pass
                        time.sleep(wiatTimeInsecs)
                finally:
                    lock.release()
                

        def stringReceived(self, msg):
            lock.acquire()
            try:
                self.inQueue.put(msg)
                self.sentMsg = self.sentMsg - 1
                print self.ip, 'add to inqueue'  
                
            finally:
                lock.release()
                
        def sendMessage(self, msg):
            try:    
                self.sendString(msg)
            except :
                print '((((((((((((((((((((((((((((((((((((((((((((Error', self.ip    
                print "((((((((((((((((((((((((((((((((((((((((((((Unexpected error:", sys.exc_info()[0]
                tcpManager.RemoveClient(self)   
                tcpManager.addToQueue(msg)        
                    

                
        def canAddMsgToOutQueue(self):
            canAdd = False    
            canAdd = True if self.maxNumberOfMsgs > self.sentMsg else False
            return canAdd



class TCPQueueConnectorClient(BaseQueueConnector):
 
    def __init__(self, configuration,logWriter=None):
        self._Configuration = configuration
        self._logWriter = logWriter
       
        self.inq = Queue.Queue()
        self.outq = Queue.Queue()
        self.__initConnectionsToServers()
    
    def addToQueue(self, strdata):
        while not self.__canAddNewMsg():        
            print  '@@@queues is full@@@'    
            time.sleep(wiatTimeInsecs)
            
        self.outq.put(strdata)
           
    
    def tryToGet(self):
        if not  self.inq.empty():
            return self.inq.get()
        else:
            return None

    def GetInQueueSize(self):
        print self.inq.qsize()

    def RemoveClient(self,tcpClientToRemove):
        self.__connections.remove(self)
        
    def __initConnectionsToServers(self):
        self.__connections = []       
        servers = self._Configuration.servers        
        for server in servers:
            point = TCP4ClientEndpoint(reactor, server.ip, server.port)
            print server.ip, server.port ,server.maxNumberOfMsg
            connector = TCPClient(self, server.ip,self.inq,self.outq, server.maxNumberOfMsg)
            self.__connections.append(connector)    
            d = connectProtocol(point, connector)
        Thread(target=reactor.run, args=(False,)).start()

    def __canAddNewMsg(self):
        canAdd = False
        lock.acquire()    
        try:         
            for ser in self.__connections:    
                canAdd = canAdd or ser.canAddMsgToOutQueue()
        finally:
            lock.release()
        return canAdd
               
                
class TCPServer(basic.Int32StringReceiver):

    __processMsgFunction = None    
    def __init__(self, processMsgFunction):
        self.__processMsgFunction = processMsgFunction
        self.__messageCounter = 0
          
    def stringReceived(self, msg):
        dataToSend = self.__processMsgFunction(msg)    
        print '-------------' ,self.__messageCounter,'-------------'
        self.__messageCounter = self.__messageCounter  + 1
        self.sendDataBack(dataToSend)
            
    def sendDataBack(self,data):
        #print ':: sending data'
        self.sendString(data)
        self.__messageCounter = self.__messageCounter  - 1

class TCPServerFactory(protocol.Factory):
         
    __processMsgFunction = None   
    def __init__(self, processMsgFunction):
        self.__processMsgFunction = processMsgFunction      

    def buildProtocol(self, addr):
        return TCPServer(self.__processMsgFunction)      


class TCPQueueConnectorServer(BaseQueueConnector):
 
    def __init__(self,processMsgFunction, configuration,logWriter=None):
        self._Configuration = configuration
        self._logWriter = logWriter
        self.__processMsgFunction = processMsgFunction
        self.__initServer()
   
    def Stop():
        reactor.stop()
        
    def __initServer(self):
        serverPort = "tcp:%i" %self._Configuration.port       
        print serverPort
        endpoints.serverFromString(reactor, serverPort).listen(TCPServerFactory(self.__processMsgFunction))                  
        print "starting"
        reactor.run()
      

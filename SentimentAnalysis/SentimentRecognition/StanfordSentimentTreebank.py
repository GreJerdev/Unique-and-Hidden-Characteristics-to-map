import socket


class SentimentRecognitionStanfordSentimentTreebank:

    def __init__(self, config):
        ip = '127.0.0.1'
        port = 6789
        if config != None or config.ip != None or len(config.ip) > 0:
            ip = config.ip
        if config != None and config.port != None:
            port = config.port
        print('port type:',type(port)
        self.ip = ip
        self.port = port

    def GetSentiments(self, dataToSend):
        
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((self.ip, self.port))
        ignorData = False;
        dataToSend = dataToSend + "!@@!"
        print '****'
        try:
            for c in dataToSend:
                c = c.encode('UTF-8')
                client_socket.send(c)
        except Exception, e:
                client_socket.send("!@@!")
                print "*******Error "+ str(e)
                ignorData = True
        data=str("")
        counter = 0
        massgesize = 100000
        getMassgesize = False
        print 'data sent'
        print '****'
        while 1:
            revData = client_socket.recv(1)
            data = data + revData
            arr = data.split("|")
            if len (arr) > 1 and not getMassgesize:
                massgesize = int(arr[0])
                getMassgesize = True
                data = arr[1]
            if massgesize == len(data):
                break
        client_socket.close()
        if ignorData == True:
            raise NameError('bad data')
        return data

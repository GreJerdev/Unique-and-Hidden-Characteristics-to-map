from SentimentRecognitionStanfordSentimentTreebank import SentimentRecognitionStanfordSentimentTreebank


def GetSentimentRecognition(configXml):
    config = type('config', (object,), {}) 
    config.ip = configXml.sentimentprocessuint.sentimentrecognition.ip.string
    strport = configXml.sentimentprocessuint.sentimentrecognition.port.string
    config.port = int(strport,10)
    return SentimentRecognitionStanfordSentimentTreebank(config)

from bs4 import BeautifulSoup

def GetConfiguraton(logWriter=None):
    soup = BeautifulSoup(open("config.xml"), 'html.parser')
    return soup


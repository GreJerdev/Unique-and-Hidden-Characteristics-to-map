
from configurationLoader import GetConfiguraton
from SoureDataManager import FactorySoureDataManager

configXml = GetConfiguraton(None)

sourceDBProvider = FactorySoureDataManager.GetSourceDataManager(configXml)
susDBProvider = FactorySoureDataManager.GetSUSDataManager(configXml)


import mysql.connector
from BaseSoureDataManager import BaseSoureDataManager
from mysql.connector import Error

class Command(object):

    def __init__(self,procName = None, args = None):
        self._procName = procName
        self._args = args
    
    @property
    def ProcName(self):
        return self._procName

    @ProcName.setter
    def ProcName(self, value):
        self._procName = value

    @property
    def Args(self):
        return self._args

    @Args.setter
    def Args (self, value):
        self._args =  value

class mySQLSoureDataManager(BaseSoureDataManager):
 
    def __init__(self, configuration,logWriter=None):
        self._Configuration = configuration
        self._logWriter = logWriter

    def WriteLog(self, logLevel, message):
        if not(self._logWriter is None) :
           self._logWriter.WriteLog(logLevel,message)
        else:
           print(message)

    def GetItemsByCostomFilter(self, params):
        args = (params.lat,params.lon,params.dis)
        return self.__CallProcWithParameter('usp_get_restorans_by_location',args)

    def GetRestaurantInfo(self, idsList):
        listOfCommands = list()
        for id in idsList:
            listOfCommands.append(Command('usp_get_restaurant_info',(id,)))    
        return self.__CallProcWithParameterBulk(listOfCommands)
           
        
    def GetAllItems(self):
        return self.__CallProcWithParameter('usp_get_all_restorans',())
       
    def __ExecuteQuery(self, query, args=None):
        results = list()
        try:
            cnx = mysql.connector.connect(user=self._Configuration.user, 
            password=self._Configuration.password, 
            host=self._Configuration.host, database=self._Configuration.databaseName)
            cursor = cnx.cursor()
            cursor.execute(query,args)
            results = list(cursor)
            cnx.commit()
           
        except Error as e:
            self.WriteLog(4, e) 
        finally:
            cursor.close()
            cnx.close()
       
        return results

    def __CallProcWithParameterBulk(self,listCommandsAndParameters):
        retVals = list()
        try:
            conn = mysql.connector.connect(user=self._Configuration.user, 
            password=self._Configuration.password, 
            host=self._Configuration.host, database=self._Configuration.databaseName)
            cursor = conn.cursor()

            for commandAndParameters in listCommandsAndParameters:
                cursor.callproc(commandAndParameters.ProcName, commandAndParameters.Args)
                cursor.fetchone()
                results = cursor.stored_results()
                for result in results:
                    table = list()
                    for row in result:
                        table.append(row)
                    retVals.append(table)

            conn.commit()
        except Error as e:
            self.WriteLog(4, e) 
             
        finally:
            cursor.close()
            conn.close()
        return retVals
  
    def __CallProcWithParameter(self,procName,args):
        retVals = list()
        try:
            conn = mysql.connector.connect(user=self._Configuration.user, 
            password=self._Configuration.password, 
            host=self._Configuration.host, database=self._Configuration.databaseName)
            cursor = conn.cursor()
 
            cursor.callproc(procName, args)
            cursor.fetchone()
            results = cursor.stored_results()
            
            for result in results:
                table = list()
                for row in result:
                    table.append(row)
                retVals.append(table)
                
            conn.commit()
        except Error as e:
            self.WriteLog(4, e) 
             
        finally:
            cursor.close()
            conn.close()
        return retVals

   
    
            

            

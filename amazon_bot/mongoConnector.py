
from pymongo import MongoClient
import sys

class MongoConnector:

    __mongo_url = "mongodb+srv://admin:eGpCz4XWJ2r1FU3T@amzdlsd01-qfqmt.mongodb.net/authSource=amzdlsd01&retryWrites=true&w=majority"
    __db = None

    def __init__(self):
        client = MongoClient(self.__mongo_url, ssl=True)
        self.__db = client['amzdlsd01']

    def insertItems(self, data, collection): 
        res = self.__db[collection].insert_many(data)
        return res

    def deleteOlder(self, collection): 
        listOfTimestamp = self.__db[collection].distinct("timestamp")
        lenOfTmp = len(listOfTimestamp)
        query_to_apply = { "timestamp" : { "$lt": int(listOfTimestamp[lenOfTmp - 2]) } }

        if(lenOfTmp > 2):
            try:
                self.__db[collection].delete_many(query_to_apply)
            except:
                e = sys.exc_info()
                print("problem with the deletemany query", e)
        return 0

    def getAllItems(self, collection): 
        return self.__db[collection].find({})

    
    def getPreviousItems(self, collection):
        listOfTimestamp = self.__db[collection].distinct("timestamp")
        lenOfTmp = len(listOfTimestamp)
        if(lenOfTmp >= 2):
            prevTimespan = int(listOfTimestamp[lenOfTmp - 2])
            return self.__db[collection].find({"timestamp": prevTimespan})
        else:
            return self.getAllItems(collection)

    def getLastItems(self, collection):
        listOfTimestamp = self.__db[collection].distinct("timestamp")
        lenOfTmp = len(listOfTimestamp)
        if(lenOfTmp >= 1):
            lastTimestamp = int(listOfTimestamp[lenOfTmp - 1])
            return self.__db[collection].find({"timestamp": lastTimestamp})
        else: 
            return self.getAllItems(collection)

            

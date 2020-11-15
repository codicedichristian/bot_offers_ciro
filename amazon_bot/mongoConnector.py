
from pymongo import MongoClient
import sys


class MongoConnector:

    __messageToCategory = {
        "Get tech" : "BEST_LAUNCH_ELECTR_HOURLY",
        "Get tech 24h" : "BEST_SELLER_ELECTR_HOURLY_24H",
        "Get Messages":"ITEMS_DIFF", 
        "Get grocery 24h":"BEST_SELLER_GROCER_HOURLY_24H", 
        "Get kitchen 24h":"BEST_SELLER_KITCHE_HOURLY_24H", 
        "Get kitchen":"BEST_LAUNCH_KITCHE_HOURLY", 
        "Get tools 24h":"BEST_SELLER_TOOLSS_HOURLY_24H", 
        "Get computer 24h":"BEST_SELLER_COMPUT_HOURLY_24H", 
        "Get sports 24h":"BEST_SELLER_SPORTS_HOURLY_24H", 
        "Get foodnb":"BEST_LAUNCH_FOODNB_HOURLY", 
        "Get lights":"BEST_SELLER_LIGHTI_HOURLY",
        "Get hcp":"BEST_SELLER_HCPHCP_HOURLY"
    }

    __db = None
    __mongoConnection = 'mongodb+srv://admin:r47eTLplxKiEp4Jj@amzdlsd01-qfqmt.mongodb.net/authSource=amzdlsd01&retryWrites=true&w=majority'

    def __init__(self):
        client = MongoClient(self.__mongoConnection, ssl=True)
        self.__db = client['amzdlsd01']

    # insert items if the data input is consistent
    def insertItems(self, data, collection): 
        res = self.__db[collection].insert_many(data)
        return res

    # delete the last but two of items in the given collection
    def deleteOlder(self, collection): 
        listOfTimestamp = self.__db[collection].distinct("timestamp")
        lenOfTmp = len(listOfTimestamp)

        if(lenOfTmp > 2):
            query_to_apply = { "timestamp" : { "$lt": int(listOfTimestamp[lenOfTmp - 2]) } }
            try:
                self.__db[collection].delete_many(query_to_apply)
            except:
                e = sys.exc_info()
                print("problem with the deletemany query", e)
        
        print("delete older things of", collection)
        return 0

    # get all items of given collection
    def getAllItems(self, collection): 
        return self.__db[collection].find({})

    # get the previus timestamp items of given collection
    def getPreviousItems(self, collection):
        listOfTimestamp = self.__db[collection].distinct("timestamp")
        lenOfTmp = len(listOfTimestamp)
        if(lenOfTmp >= 2):
            prevTimespan = int(listOfTimestamp[lenOfTmp - 2])
            return self.__db[collection].find({"timestamp": prevTimespan})
        else:
            return self.getAllItems(collection)

    # get last timestamp items of a given collection
    def getLastItems(self, text, from_message=False):
        if(from_message == True) :
            collection=self.__messageToCategory[text]
        else:
            collection=text
        
        listOfTimestamp = self.__db[collection].distinct("timestamp")
        lenOfTmp = len(listOfTimestamp)
        if(lenOfTmp >= 1):
            lastTimestamp = int(listOfTimestamp[lenOfTmp - 1])
            return self.__db[collection].find({"timestamp": lastTimestamp})
        else: 
            return self.getAllItems(collection)

            

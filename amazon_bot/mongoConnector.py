
from pymongo import MongoClient
import sys


class MongoConnector:

    __messageToCategory = {
        "mangiare"    : "BEST_SELLER_GROCER_HOURLY_24H",
        "cucina"      : "BEST_SELLER_KITCHE_HOURLY_24H",
        "elettronica" : "BEST_SELLER_ELECTR_HOURLY_24H",
        "tools"       : "BEST_SELLER_TOOLSS_HOURLY_24H", 
        "computer"    : "BEST_SELLER_COMPUT_HOURLY_24H", 
        "sports"      : "BEST_SELLER_SPORTS_HOURLY_24H", 
        "boost"       : "BEST_SELLER_BOOSTT_HOURLY_24H", 
        "mix pg1"     : "DEALS_BEST_SELLER_MIX____HOURLY_PG1", 
        "mix pg2"     : "DEALS_BEST_SELLER_MIX____HOURLY_PG2", 
        "mix pg3"     : "DEALS_BEST_SELLER_MIX____HOURLY_PG3",
        "mix pg4"     : "DEALS_BEST_SELLER_MIX____HOURLY_PG4",
        "mix pg5"     : "DEALS_BEST_SELLER_MIX____HOURLY_PG5",
        "mix pg6"     : "DEALS_BEST_SELLER_MIX____HOURLY_PG6",
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
    
    def insertOneItem(self, data, collection): 
        res = self.__db[collection].insert_one(data)
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

    def deleteAll(self, collection): 
        self.__db[collection].delete_many({})
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

            

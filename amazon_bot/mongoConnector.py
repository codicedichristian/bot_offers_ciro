
from pymongo import MongoClient


class MongoConnector:

    __mongo_url = "mongodb+srv://admin:eGpCz4XWJ2r1FU3T@amzdlsd01-qfqmt.mongodb.net/authSource=amzdlsd01&retryWrites=true&w=majority"
    __db = None

    def __init__(self):
        client = MongoClient(self.__mongo_url, ssl=True)
        self.__db = client['amzdlsd01']

    def inserisciRoba(self, data, collection): 
        res = self.__db[collection].insert_many(data)
        return res
    
    def pulisciRoba(self, collection): 
        ## TODO pulire roba vecchia delete many all 



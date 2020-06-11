
import pymongo


client = pymongo.MongoClient("mongodb+srv://christian:<password>@amzdlsd01-qfqmt.mongodb.net/<dbname>?retryWrites=true&w=majority")
db = client.test


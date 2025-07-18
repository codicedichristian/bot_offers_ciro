


# ## new imports
from amazonList import AmazonList
from mongoConnector import MongoConnector
import time
from datetime import datetime

def checkKey(dict, key): 
      
    if key in dict: 
        return True
    else: 
       return False

## newItems - oldItems = items added (just new items)
def myBeautifulDiff(oldItems, newItems):
    asins = [item['asin'] for item in list(oldItems)]
    diff = []
    for item in list(newItems):
        if item['asin'] not in asins:
            diff.append(item)
    return diff



categories = (
        "DEALS_BEST_SELLER_MIX____HOURLY_PG1",
        "DEALS_BEST_SELLER_MIX____HOURLY_PG2",
        "DEALS_BEST_SELLER_MIX____HOURLY_PG3",
        "DEALS_BEST_SELLER_MIX____HOURLY_PG4",
        "DEALS_BEST_SELLER_MIX____HOURLY_PG5",
        "DEALS_BEST_SELLER_MIX____HOURLY_PG6",
        "BEST_SELLER_GROCER_HOURLY_24H", 
        "BEST_SELLER_KITCHE_HOURLY_24H", 
        "BEST_SELLER_ELECTR_HOURLY_24H", 
        "BEST_SELLER_TOOLSS_HOURLY_24H", 
        "BEST_SELLER_COMPUT_HOURLY_24H", 
        "BEST_SELLER_SPORTS_HOURLY_24H", 
        #new 
        "BEST_SELLER_BOOSTT_HOURLY_24H",

    )

diff_collection = "ITEMS_DIFF"
    

def main():

    amListObj = AmazonList()
    try: 
        mongo = MongoConnector()
    except: 
        print("exception in mongoconnector, we will retry it next time.")
        return


    # for category in categories:
    #     items_from_amazon = amListObj.getNewList(category) ## return json obj list
    #     res = mongo.insertItems(items_from_amazon, category)
    #     print(res)
    for category in categories:
        print("getting new list from: ", category)
        # get list from amazon html
        try: 
            items_from_amazon = amListObj.getNewList(category)
            ## put the list inside mongodb 
            mongo.insertItems(items_from_amazon, category)
            ## delete older ( three timestamp before)
            print("deleting older objects from: ", category)
            items = mongo.deleteOlder(category)  
        except: 
            print("operations on: ", category, "caused an error, we will retry next time" )
            continue
    
    print("writing last timestamp...")
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    lastLaunchItem = {
        "date" : dt_string, 
    }
    mongo.deleteAll("LAST_LAUNCH")
    mongo.insertOneItem(lastLaunchItem, "LAST_LAUNCH")


if __name__ == '__main__':
    main()

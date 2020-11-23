


# ## new imports
from amazonList import AmazonList
from mongoConnector import MongoConnector
import time

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
        "DEALS_GENERAL",
        "BEST_SELLER_GROCER_HOURLY_24H",
        "BEST_SELLER_ELECTR_HOURLY_24H",
        "BEST_SELLER_TOOLSS_HOURLY_24H",
        "BEST_SELLER_KITCHE_HOURLY_24H",
        "BEST_SELLER_COMPUT_HOURLY_24H",
        "BEST_SELLER_SPORTS_HOURLY_24H",
        "BEST_SELLER_BELLEZ_HOURLY_24H",
        "BEST_SELLER_GAMESS_HOURLY_24H",
        
     )

diff_collection = "ITEMS_DIFF"
    

def main():

    amListObj = AmazonList()
    mongo = MongoConnector()

    # for category in categories:
    #     items_from_amazon = amListObj.getNewList(category) ## return json obj list
    #     res = mongo.insertItems(items_from_amazon, category)
    #     print(res)
    for category in categories:
        print("getting new list from: ", category)
        # get list from amazon html
        items_from_amazon = amListObj.getNewList(category)
        ## put the list inside mongodb 
        mongo.insertItems(items_from_amazon, category)
        ## delete older ( three timestamp before)
        print("deleting older objects from: ", category)
        items = mongo.deleteOlder(category)  
        ## get differences 
        diffToUpload = myBeautifulDiff(mongo.getPreviousItems(category), mongo.getLastItems(category, False))

        if(len(diffToUpload) > 0):
            mongo.insertItems(diffToUpload, 'ITEMS_DIFF')
        else: 
            print("there aren't diff, so we will not update ITEMS_DIFF")
        
        

        time.sleep(5)


if __name__ == '__main__':
    main()

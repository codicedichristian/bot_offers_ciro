


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
    print(diff)
    return diff



categories = (
        "BEST_SELLER_GROCER_HOURLY_24H",
        "BEST_SELLER_ELECTR_HOURLY_24H",
        "BEST_SELLER_TOOLSS_HOURLY_24H",
        "BEST_SELLER_KITCHE_HOURLY_24H",
        "BEST_SELLER_COMPUT_HOURLY_24H",
        "BEST_SELLER_SPORTS_HOURLY_24H",
    #   # "BEST_LAUNCH_GLOBAL_HOURLY",  # todo different scraping 
       "BEST_LAUNCH_ELECTR_HOURLY",
       "BEST_LAUNCH_KITCHE_HOURLY",
       "BEST_LAUNCH_FOODNB_HOURLY",
       "BEST_SELLER_GROCER_HOURLY",
       "BEST_SELLER_KITCHE_HOURLY",
       "BEST_SELLER_LIGHTI_HOURLY",
       "BEST_SELLER_ELECTR_HOURLY",
       "BEST_SELLER_HCPHCP_HOURLY"
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
        
    

    ## __________ 

    # - i diff li mettiamo tutti nella stessa collection "diff" 
    # - gestire i diff (solo una collection o piu' collections?/inserire la version?)
    # - gestire le versioni dei diff se si vuole... oppure si cancella tutto ogni giro
    # - rimettere in piedi il loop e fare una bella prova con i diff compresi!
    # - guardare come farlo fare automatico ogni due ore

    # - fatto questo bisogna attaccare il bot che si legge gli elementi dal diff e che li sputa in un formato bello (con il bottone pubblica)

    # - finito tutto colleghiamo i pezzi: 
    #     1- tirare nuova lista giu di 5 elementi da amazon ogni 2 ore
    #     2- confrontare con la lista presente su mongo
    #     3- tirare fuori le diff e metterle sulla collection diff
    
    # - bot che ogni 2 ore e 15 min controlla la lista diff e spara sulla chat personale i prodotti :) 
    


if __name__ == '__main__':
    main()

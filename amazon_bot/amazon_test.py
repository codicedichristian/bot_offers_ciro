


# ## new imports
import json
from jsonStorageManager import JsonStorageManager
from amazonList import AmazonList
from deepdiff import DeepDiff
from mongoConnector import MongoConnector

def checkKey(dict, key): 
      
    if key in dict: 
        return True
    else: 
       return False

def spacchettamento_diff(diff):
    new_list = []
    print(diff)
    if(checkKey(diff, "iterable_item_added")):
        set_of_values_added = diff['iterable_item_added']
        for key in list(set_of_values_added):
            new_list.append(diff['iterable_item_added'][key])
        return new_list
    else:
        print("no diff")
    print(new_list)
    return 0


categories = (
       "BEST_SELLER_GROCER_HOURLY_24H",
       "BEST_SELLER_ELECTR_HOURLY_24H",
       "BEST_SELLER_TOOLSS_HOURLY_24H",
       "BEST_SELLER_KITCHE_HOURLY_24H",
       "BEST_SELLER_COMPUT_HOURLY_24H",
       "BEST_SELLER_SPORTS_HOURLY_24H",
       "BEST_LAUNCH_GLOBAL_HOURLY",
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

    # get list from amazon html
    items_from_amazon = amListObj.getNewList('BEST_LAUNCH_GLOBAL_HOURLY')
    ## put the list inside mongodb 
    mongo.insertItems(items_from_amazon, 'BEST_LAUNCH_GLOBAL_HOURLY')
    ## delete older ( three timestamp before)
    items = mongo.deleteOlder('BEST_LAUNCH_GLOBAL_HOURLY')  
    ## get differences 
    ddiff = DeepDiff(mongo.getPreviousItems('BEST_LAUNCH_GLOBAL_HOURLY'), mongo.getLastItems('BEST_LAUNCH_GLOBAL_HOURLY'))
    
    print(spacchettamento_diff(ddiff))
    amListObj.closeDriver()

    ## __________ 

     
    # - ora dobbiamo tirare giu gli elementi da mongodb del previous timestamp e
    #  confrontarli con mongodb lasttimestamp

    # - trovato il diff aggiorniamo la lista su mongo (facile passaggio perchè gia testato)
    # - i diff li mettiamo tutti nella stessa collection "diff" 
    
    # - fatto questo bisogna attaccare il bot che si legge gli elementi dal diff e che li sputa in un formato bello (con il bottone pubblica)


    # - finito tutto colleghiamo i pezzi: 
    #     1- tirare nuova lista giu di 5 elementi da amazon ogni 2 ore
    #     2- confrontare con la lista presente su mongo
    #     3- tirare fuori le diff e metterle sulla collection diff
    
    # - bot che ogni 2 ore e 15 min controlla la lista diff e spara sulla chat personale i prodotti :) 
    

    


if __name__ == '__main__':
    main()

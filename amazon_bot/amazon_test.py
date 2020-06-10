


# ## new imports
import json
from jsonStorageManager import JsonStorageManager
from amazonList import AmazonList
from deepdiff import DeepDiff

def checkKey(dict, key): 
      
    if key in dict: 
        return True
    else: 
       return False

def spacchettamento_diff(diff):
    new_list = []
    if(checkKey(diff, "iterable_item_added")):
        set_of_values_added = diff['iterable_item_added']
        for key in list(set_of_values_added):
            new_list.append(diff['iterable_item_added'][key])
        return new_list
    else:
        print("no diff")

    return 0

    

    

def main():

    # get 5 elements for each list from amazon 
    # TODO right now we just take one we have to implement it for others 


    # TODO -> we NEED TO GET ALSO THE ASIN we can find it in the item link. 
    # get the new list of element
    amListObj = AmazonList()
    items_from_amazon = amListObj.getNewList("BEST_SELLER_ELECTR_HOURLY_24H") ## return json obj list
    
    # print(items_from_amazon)

    # ## get the same list but from jsonStorage (the 5 element from the collection)
    # storage = JsonStorageManager()
    # items_from_storage = storage.prendiLaRoba('BEST_SELLER_ELECTR_HOURLY') ## return json obj

    # ## send items amazon to jsonStorage
    # print("storage returned:  ", storage.updateLaRoba('BEST_SELLER_ELECTR_HOURLY', items_from_amazon))

    # ## crea json con differenze all'interno
    # diff = DeepDiff(items_from_storage, items_from_amazon, ignore_order=True)

    # print(spacchettamento_diff(diff))



    ## dato due array di oggetti json bisogna ritornare la differenza (in base al titolo)


    ## put the diff in another storage (where the bot or an app will get them)



    # done -> # get 5 elements for each list on jsonstorage  (delete them after get and put the newest from amazon with timespan date)
    # -- find json library # check if there is something different ---
    # take the differences and put them in another container of json storage that the bot will check every (hh:15)
    # fine.
    
    # loop each two hours (hh:00)

    


if __name__ == '__main__':
    main()

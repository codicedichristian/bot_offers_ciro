
import json
import requests

class JsonStorageManager: 

    ## same keys as amazon list getter 
    __base_url = "https://jsonstorage.net/api/items/"
    __containers = {
        'BEST_SELLER_ELECTR_HOURLY' : 'a315e435-fdcb-4a9a-907b-5504a143d2a2'
    }
    __base_header = {"Content-Type": "application/json; charset=utf-8"}

    def __getPayload(self, data): 
        return {
            "data": data,
            "Content-Type": "application/json; charset=utf-8",
            "Data-Type": "json"
        }
    
    # salvare container ids in un file per sicurezza
    def __writeInContainerFile(self, roba_da_mettere): 
        outF = open("container_list.txt", "w")
        outF.write(roba_da_mettere)
        outF.close()

    # returns all data (with all keys) or data of key received
    def prendiLaRoba(self, collection_name): 
        r = requests.get(self.__base_url + self.__containers[collection_name])
        data_rec = r.json()
        return data_rec['data']
       

    ## when it is called is needed a valid key.
    def updateLaRoba(self, collection_name, data="{'nada': 'nada'}"):
        payload = self.__getPayload(data)
        res = requests.put(
            self.__base_url + self.__containers[collection_name], 
            data = json.dumps(payload), 
            headers = self.__base_header
        )
        return res

    def creaContainer(self, container_name='senzanome', data="{'nada':'nada'}"): 
        payload = self.__getPayload(data)
        r = requests.post(self.__base_url, data=json.dumps(payload), headers=self.__base_header)
        jsonContent = json.loads(r.content)

        ## get the last element of the uri (key)
        uriArray = jsonContent['uri'].split('/')
        uri_to_save = uriArray[len(uriArray) - 1]

        # save the info in a file an into array 
        self.__writeInContainerFile(uri_to_save)
        self.__containers[container_name] = uri_to_save

        return r
        
      
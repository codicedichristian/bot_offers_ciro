
import json
import requests

class JsonStorageManager: 

    ## same keys as amazon list getter 
    __base_url = "https://jsonstorage.net/api/items/"
    __containers = {
        'BEST_SELLER_ELECTR_HOURLY' : 'a315e435-fdcb-4a9a-907b-5504a143d2a2', 
        'BEST_SELLER_ELECTR_HOURLY_24H': '45eed063-46e7-4ae9-8a0d-359be1c31ca8'
    }
    #
    # fd3a93ce-6261-4939-af1c-2d35d737233e
    # 3743f587-4172-42c4-9ec7-2252571cf5c0
    # ac81e0c8-e92e-400f-a2f4-fc87727a27e4
    # fccbc506-da17-4109-8f53-8a3ab1ce60d9
    # a1e6bc17-eab2-4a7e-b92b-717df3c6526e
    # cc4b2174-1567-40b3-9aca-bc77f70708a8
    # 734f224c-4034-4e76-aaa3-5bfdb57828cd
    # 8495a508-c314-4a9c-bbe0-40386d6f240d
    # ee03d866-7bf2-49bb-b6c3-4c281513eab7
    # d08a3b04-5f9e-4acb-94c3-7ca14a76e509
    # 8cfa20c5-c817-4a9d-865c-5e850b280b96
    # d63b921c-e9db-4e60-abde-2c88947ed689
    # df017ee3-8583-48b6-834f-8528e1fd186a
    # 902d41a8-ae2d-49cd-9fe6-0b45682205d5
    # 1542d656-defd-4224-8225-9770163e3bf8
    
    #
    __base_header = {"Content-Type": "application/json; charset=utf-8"}

    def __getPayload(self, data): 
        return {
            "data": data,
            "Content-Type": "application/json; charset=utf-8",
            "Data-Type": "json"
        }
    
    # salvare container ids in un file per sicurezza
    def __writeInContainerFile(self, roba_da_mettere): 
        with open("container_list.txt", "a") as myfile:
            myfile.write(roba_da_mettere + "\n")

    # returns all data (with all keys) or data of key received
    def prendiLaRoba(self, collection_name): 
        r = requests.get(self.__base_url + self.__containers[collection_name])
        data_rec = r.json()
        return data_rec['data']
       

    ## when it is called is needed a valid key.
    def updateLaRoba(self, collection_name, data="{'nada': 'nada'}"):
        print(data)
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
        
      
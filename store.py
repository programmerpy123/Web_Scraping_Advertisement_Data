#strategy design pattern
import json
from abc import ABC,abstractmethod
from mongo import MongoDatabse
from config import crawl
class StorageAbstract(ABC):

    @abstractmethod
    def store(self,data,*args):
        pass
    @abstractmethod
    def load(self,*args,**kwargs):
        pass


class MongoStorage(StorageAbstract):
    def __init__(self):
        self.mongo = MongoDatabse()

    def store(self,data,collection,*args):
        # collection = getattr(self.mongo.database,collection)
        collection = self.mongo.database[collection]
        if isinstance(data, list) and len(data) > 1:
             # change data['check_dup']=True
            for da in data:
                check = collection.find({'url': da["url"]})
                if check != None:
                    collection.insert_one(da)


            # collection.insert_many(data)
        else:
            collection.insert_one(data)
            print(data['post_id'])


    def load(self,collection_name,filter_para=None):
        collection_name = self.mongo.database[collection_name]
        if filter_para is not  None:
            return collection_name.find(filter_para)
        return collection_name.find()




    def update_flag(self, data):
        """"""
        self.mongo.database.advertisement_links.find_one_and_update(
            {'_id': data['_id']},
            {'$set': {'flag': True}}
        )




class FileStorage(StorageAbstract):
    def store(self,data,filename,*args):
        if crawl == 'find':
            val = ""
        else:
            val = "adv/"
        with open(f'storage/{val}{filename}.json', 'w') as f:
                 json.dump(data, f, indent=2)


    def load(self):
        with open('storage/advertisement_links.json', 'r') as f:
            links = json.loads(f.read())
            return links

    def update_flag(self):
        pass
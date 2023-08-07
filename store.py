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
    def load(self):
        pass


class MongoStorage(StorageAbstract):
    def __init__(self):
        self.mongo = MongoDatabse()

    def store(self,data,collection,*args):
        # collection = getattr(self.mongo.database,collection)
        collection = self.mongo.database[collection]
        if isinstance(data, list) and len(data) > 1:
            collection.insert_many(data)
        else:
            collection.insert_one(data)
            print(data['post_id'])

    def load(self):
        return self.mongo.database.advertisement_links.find()



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
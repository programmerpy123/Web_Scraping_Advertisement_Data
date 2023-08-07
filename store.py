#strategy design pattern
import json
from abc import ABC,abstractmethod

class StorageAbstract(ABC):

    @abstractmethod
    def store(self,data,*args):
        pass


class MongoStorage(StorageAbstract):
    def __init__(self):
        pass
    def store(self,data,*args):
        pass



class FileStorage(StorageAbstract):
    def store(self,data,filename,*args):
        with open(f'storage/adv/{filename}.json', 'w') as f:
            json.dump(data, f, indent=2)
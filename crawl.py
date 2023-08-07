import json
from abc import ABC, abstractmethod

import requests
from bs4 import BeautifulSoup
from config import BASE_LINK, CITIES, STORAGE_TYPE
from parser_page import AdvertisementPageParser
from store import FileStorage,MongoStorage

class BaseCrawler(ABC):
    def __init__(self):
        self.storage = self.__set_storage()

    @staticmethod
    def __set_storage():
        if STORAGE_TYPE == 'mongo':
            return MongoStorage()
        return FileStorage()


    @abstractmethod
    def start(self,store=False):
        pass

    @abstractmethod
    def store(self,data,filename=None):
        pass

    @staticmethod
    def get_pages(url,start=None):
        try:
            if start != 0 and start != None:
                response = requests.get(url).text
                chck_res = requests.get(url).text
                if response == chck_res:
                    return None

            elif start == None or start == 0:
                try:
                    return requests.get(url)
                except requests.HTTPError:
                    return None

        except:
            return None




class LinkCrawler(BaseCrawler):
    def __init__(self,cities):
        super().__init__()
        self.cities = cities


    def find_links(self, doc, city):
        res = BeautifulSoup(doc, 'html.parser')
        result = set()
        anchor_tags = res.find_all('a', href=lambda href: href and href.startswith(f"https://{city}.craigslist.org/"))
        for link in anchor_tags:
            if link.parent.name == 'li' and 'result-row' in link.parent.get('class',[]):
                    result.add(link)

        return result

    def start_crawl_city(self, url_address, city):
        start = 0
        final_list = []
        while True:
            result = self.get_pages(url_address.format(city, str(start)),start)

            if result == None:
                break
            final_list.extend(self.find_links(result.text, city))
            start += 1

            # crawl = bool(len(find_links(result.text)))
        #
        # for link in set(final_list):
        #     print(link.get('href'))

        print(len(set((final_list))))
        return final_list

    def start(self,store=False):
        url_address = BASE_LINK
        adv_list = list()
        for city in self.cities:
            print("link of", city)
            links = self.start_crawl_city(url_address, city)
            adv_list.extend(links)
        if store:
             self.store([{"url": i.get('href'), "flag": False} for i in adv_list])
        return adv_list


    def store(self, data,*args):
        self.storage.store(data,'advertisement_links')

class DataCrawler(BaseCrawler):

    def __init__(self):
         super(DataCrawler, self).__init__()
         self.links = self.__load_links()
         self.parser = AdvertisementPageParser()

    def __load_links(self):
          return self.storage.load()

    def start(self,store=False):
        for link in self.links:
            print(link)
            response = self.get_pages(link['url'])
            data = self.parser.parse(response.text)
            if store:
                self.store(data,data.get('post_id','sample'))

    def store(self,data,filename):
        self.storage.store(data,'advertisement_data')




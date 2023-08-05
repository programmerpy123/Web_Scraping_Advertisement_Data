import json
from abc import ABC, abstractmethod

import requests
from bs4 import BeautifulSoup
from config import BASE_LINK, CITIES
from parser_page import AdvertisementPageParser


class BaseCrawler(ABC):
    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def store(self,data,store=False):
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

    def start(self):
        url_address = BASE_LINK
        adv_list = list()
        for city in self.cities:
            print("link of", city)
            links = self.start_crawl_city(url_address, city)
            adv_list.extend(links)
        self.store([i.get('href') for i in adv_list])


    def store(self, data):
        with open('storage/data.json','w') as f:
            json.dump(data,f, indent=2)


class DataCrawler(BaseCrawler):

    def __init__(self):
         self.links = self.__load_links()
         self.parser = AdvertisementPageParser()

    @staticmethod
    def __load_links():
        with open('storage/data.json', 'r') as f:
            links = json.loads(f.read())
            return links

    def start(self):
        for link in self.links:
            response = self.get_pages(link)
            data = self.parser.parse(response.text)
            self.store()

    def store(self,data):
        pass




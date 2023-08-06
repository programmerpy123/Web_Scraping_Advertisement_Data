import re

from bs4 import BeautifulSoup


class AdvertisementPageParser:
    def __init__(self):
        self.soup =None
        self.data =None
    @property
    def title(self):
        title =  self.soup.find('span',attrs={'id':'titletextonly'})
        if title:
            return title.text
        return None

    @property
    def price(self):
        # price =  self.soup.find('span',attrs={'class':'price'})
        price_selector = 'body > section > section > h1 > span > span.price'
        price = self.soup.select_one(price_selector)
        if price:
            return price.text
        return None

    @property
    def body(self):
        body = self.soup.select_one('#postingbody')
        if body:
            return body.text
        return None

    @property
    def post_id(self):
        post_id_selector = 'body > section > section > section > div.postinginfos > p:nth-child(1)'
        post_id_tag = self.soup.select_one(post_id_selector)
        if post_id_tag:
            post_id = post_id_tag.text.replace('Id publi: ','')
            return post_id
        else:
            return None

    @property
    def create_time(self):
        created_time_selector = 'body > section > section > section > div.postinginfos > p:nth-child(2) > time'
        create_time = self.soup.select_one(created_time_selector)
        if create_time:
             return create_time.get('datetime')
        return None

    @property
    def modified_time(self):
        modified_time_selector = 'body > section > section > section > div.postinginfos > p:nth-child(3) > time'
        modified_time = self.soup.select_one(modified_time_selector)
        if modified_time:
             return modified_time.get('datetime')
        else:
            return None

    def parse(self,html_data):
        self.soup = BeautifulSoup(html_data,'html.parser')
        self.data = dict(
            title = self.title, price = self.price, body = self.body,post_id = self.post_id,
            created_time = self.create_time, modified_time = self.modified_time
        )

        return self.data







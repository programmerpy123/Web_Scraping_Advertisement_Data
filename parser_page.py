import re

from bs4 import BeautifulSoup


class AdvertisementPageParser:
    def __init__(self):
        self.soup =None
        self.data =None
    @property
    def title(self):
        return  self.soup.find('span',attrs={'id':'titletextonly'})

    @property
    def price(self):
        return self.soup.find('span',attrs={'class':'price'})

    @property
    def body(self):
        return self.soup.select_one('#postingbody')

    @property
    def post_id(self):
        post_id_selector = 'body > section > section > section > div.postinginfos > p:nth-child(1)'
        post_id_tag = self.soup.select_one(post_id_selector).text
        if post_id_tag:
            post_id = post_id_tag.replace('Id publi: ','')
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
            title = self.title.text, price = self.price.text, body = self.body.text,post_id = self.post_id,
            created_time = self.create_time, modified_time = self.modified_time
        )

        return self.data







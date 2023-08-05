from bs4 import BeautifulSoup


class AdvertisementPageParser:
    def parse(self,html_data):
        soup = BeautifulSoup(html_data,'html_parser')
        data = dict(
            title = None, price = None, body = None,post_id = None,
            created_time = None, modified_time = None
        )




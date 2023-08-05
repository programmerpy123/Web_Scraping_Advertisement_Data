import sys

import requests
from bs4 import BeautifulSoup
from crawl import LinkCrawler
from config import CITIES
from crawl import DataCrawler


if __name__ == "__main__":
    switch = sys.argv[1]
    if switch == 'find_links':
      LinkCrawler(CITIES).start()
    elif switch == 'extract_pages':
        DataCrawler().start()
    else:
        raise SystemError






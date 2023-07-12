from abc import ABC, abstractmethod
import requests
from bs4 import BeautifulSoup

class AbstractCollector(ABC):
    target_url = ""
    downloader = None
    
    def __init__(self, url):
        self.target_url = url
    
    def set_target_url(self, url):
        self.target_url = url

    def get_target_url(self):
        return self.target_url
    
    def get_soup(self, url):
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        # print(soup.prettify())
        return soup

    @abstractmethod
    def fetch_papers(self):
        pass
    
    @abstractmethod
    def handle_exception(self):
        pass
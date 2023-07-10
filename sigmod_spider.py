from abstract_spider import AbstractSpider
import requests
from bs4 import BeautifulSoup

class SigmodSpider(AbstractSpider):
    def __init__(self, url):
        super().__init__(url)

    # 从self.target中获取论文url列表
    def get_paper_url_list(self):
        r = requests.get(self.target_url)
        soup = BeautifulSoup(r.text, 'html.parser')
        print(soup.prettify())
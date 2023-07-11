from .collector import AbstractCollector
from downloader import AcmDownloader
import requests
from bs4 import BeautifulSoup
import os
from time import sleep

class DblpCollector(AbstractCollector):
    __url_list = {}
    __error_list = {}

    def __init__(self, url):
        super().__init__(url)
        self.downloader = AcmDownloader()
        self.__crawl_list_from_dblp()

    # 从self.target_url中获取论文url列表
    def __crawl_list_from_dblp(self):
        soup = self.get_soup(self.target_url)
        # 找到所有类名为"h2"的结点，获取其文本
        # h2_list = soup.find_all("h2")
        h2_list = [h2.text for h2 in soup.find_all("h2") if h2.text != "Refine list"]
        # 找到所有class为"pub-list"的ul结点
        pub_list = soup.find_all("ul", "publ-list")[1:]
        if len(h2_list) != len(pub_list):
            print(len(h2_list), len(pub_list))
            raise Exception("h2_list and pub_list not match")

        for i in range(len(h2_list)):
            # 获取h2_list中的第i个结点的子节点的文本
            session = h2_list[i]
            self.__url_list[session] = {}
            cur_session = self.__url_list[session]
            # 遍历pub_list中每一个li结点
            for li in pub_list[i].find_all("li", "entry inproceedings"):
                paper_url = li.select("nav > ul > li:nth-child(1) > div.head > a")[0].get("href")
                paper_title = li.select("cite > span.title")[0].text.strip(".")
                print("session:%s, paper_title:%s, paper_url:%s" % (session, paper_title, paper_url))
                cur_session[paper_title] = paper_url
    
    def fetch_papers(self):
        for session in self.__url_list.keys():
            for paper_title in self.__url_list[session].keys():
                paper_url = self.__url_list[session][paper_title]
                try:
                    self.downloader.download_paper_from_url(session, paper_title, paper_url)
                    sleep(5)
                except Exception as ex:
                    print("download_papers: failed:%s" % ex)
                    self.__error_list[paper_title] = paper_url
                    # raise Exception("download_papers error!")
    
    def handle_exception(self):
        print("handle_exception: error_list:%s" % self.__error_list)


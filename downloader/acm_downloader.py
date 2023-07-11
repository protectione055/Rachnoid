from .downloader import AbstractDownloader
from bs4 import BeautifulSoup
import requests
import os

class AcmDownloader(AbstractDownloader):
    def __init__(self):
        self.header = {}
        self.header["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        # Todo: 改为从config.json中读取Cookie
        self.header["Cookie"] = r"MAID=GphEyjNrYdmBOs1ez5FyJQ==; _ga=GA1.2.1749652940.1687833526; _hjSessionUser_1290436=eyJpZCI6IjAxYjQ5MGE1LWEyMGQtNWQ5Mi05MjU0LWZkMTBmNGE4OGYwNyIsImNyZWF0ZWQiOjE2ODc4MzM1MjY4NDcsImV4aXN0aW5nIjp0cnVlfQ==; cookiePolicy=accept; _gid=GA1.2.256784231.1688955371; SERVER=WZ6myaEXBLHyk/r17lxmwg==; JSESSIONID=0a7a9cb8-bf39-49f7-9c0e-a7b7e8c5c8fc; MACHINE_LAST_SEEN=2023-07-10T07%3A23%3A23.651-07%3A00; _ga_JPDX9GZR59=GS1.2.1688999005.9.0.1688999005.0.0.0; _hp2_id.1083010732=%7B%22userId%22%3A%221712104309718408%22%2C%22pageviewId%22%3A%222709239663216717%22%2C%22sessionId%22%3A%225366453289223299%22%2C%22identity%22%3Anull%2C%22trackerVersion%22%3A%224.0%22%7D; __cf_bm=ghSD5F7mFWAe5MsC5xdDiPdN0FyEor6WKa466DSXosA-1689004366-0-AWk7YiIx9zn3orzYw96p+c3BxRoujH2BcUbvNXv5MPXdK1wt3ITFVHI0hDAlaZV0FA0jFD/pVj3Q7G6BnhZO7TA=; _hp2_ses_props.1083010732=%7B%22ts%22%3A1689004366474%2C%22d%22%3A%22dl.acm.org%22%2C%22h%22%3A%22%2Fdoi%2F10.1145%2F3555041.3589336%22%7D"

    def download_paper_from_url(self, directory, name, url):
        name = self.get_valid_filename(name)
        if os.path.exists(directory  + "\\" + name + ".pdf"):
            return
        
        if not os.path.exists(directory):
            os.mkdir(directory)
        
        try:
            '''
            # 从通过url访问acm页面，获取pdf的url，然后下载pdf内容到文件
            soup = BeautifulSoup(acm_page.text, 'html.parser')
            
            # 从acm_page得到pdf的url
            pdf_url = soup.find("a", {"title": "PDF"}).get("href")
            '''
            # 首先需要重定向到acm的页面
            redirect_url = requests.get(url, timeout=30, headers=self.header).url
            pdf_url = redirect_url.replace("/doi/", "/doi/pdf/")
            # 获取pdf内容
            paper_content = requests.get(pdf_url, timeout=30, verify=False, headers=self.header)
            # 保存pdf内容到文件
            self.save_content_to_file(directory + "\\" + name + ".pdf", paper_content.content)
        except Exception as ex:
            print("download_paper_from_url: failed:%s" % ex)
            raise Exception("download_paper_from_url error!")
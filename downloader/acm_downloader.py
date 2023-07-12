from downloader.abstract_downloader import AbstractDownloader
from bs4 import BeautifulSoup
import requests
import os

class AcmDownloader(AbstractDownloader):
    def __init__(self):
        self.header = {}
        self.header["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        # Todo: 改为从config.json中读取Cookie
        self.header["Cookie"] = r""

    def download_paper_from_url(self, directory, name, url):
        name = self.get_valid_filename(name)
        pdf_file = os.path.join(directory, name + ".pdf")
        if os.path.exists(pdf_file):
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
            redirect_url = requests.get(url, timeout=180, headers=self.header).url
            if redirect_url.find("dl.acm") == -1:
                print("redirect_url error:%s" % redirect_url)
                raise Exception("redirect_url error!")
            pdf_url = redirect_url.replace("/doi/", "/doi/pdf/")
            # 获取pdf内容
            paper_content = requests.get(pdf_url, timeout=600, headers=self.header)
            # 保存pdf内容到文件
            self.save_content_to_file(pdf_file, paper_content.content)
        except Exception as ex:
            print("download_paper_from_url: failed:%s" % ex)
            raise Exception("download_paper_from_url error!")
import abc

# 一个抽象类，定义了一系列接口，负责从一个网站爬取列表中的论文
class AbstractSpider(meataclass=abc.ABCMeta):
    url_list = {}
    target_url = ""

    def __init__(self, url):
        self.target_url = url
    
    def set_target_url(self, url):
        self.target_url = url

    def get_target_url(self):
        return self.target_url

    @abc.abstractmethod
    def get_paper_url_list(self):
        pass 

    @abc.abstractmethod
    def download_papers(self):
        pass
    
    @abc.abstractmethod
    def handle_exception(self):
        pass
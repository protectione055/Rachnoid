import requests
import os
import json
from bs4 import BeautifulSoup
import time
requests.packages.urllib3.disable_warnings()


with open("config.json", 'r', encoding='utf-8') as json_file:
    config = json.load(json_file)
    globals().update(config["config1"])
headers = {'User-Agent': ua, 'Cookie': '', 'Referer': referer}


def get_paper(url, folder, filename):
    '''下载单篇论文
        :param url: 要下载的论文url
        :param folder: 保存在本地的路径
        :param filename: 保存在本地的文件名
    '''
    print("Starting to get paper...and save it to %s" % folder)
    try:
        if not os.path.exists(folder):  # 若文件夹不存在，则创建
            os.mkdir(folder)

        path = folder + '/' + filename
        print("file path %s" % path)
        if not os.path.exists(path):  # 若文件不存在，则创建
            print("Get paper from url: %s" % url)
            for i in range(5):
                try:
                    r = requests.get(url, timeout=30, headers=headers)
                    with open(path, 'wb') as f:
                        f.write(r.content)
                        f.close()
                        print("%s文件保存成功" % (filename))
                        return
                except Exception as ex:
                    time.sleep(5)
                    print(ex)
                    print("Retrying...")
                    continue
            print("Connection refused by the server..")
            print("Error task: " + filename)
            return
        else:
            print("%s文件已存在" % (filename))
    except Exception as e:
        print("%s:爬取失败" % (url))
        print("get_paper:" + str(e))


def getHTMLText(url):
    # Get html from acm
    try:
        if url.find("acm.org") != -1:
            r = requests.get(url, timeout=30, verify=False, headers=headers)
            if r.text.find("Shenzhen University") == -1:
                print("getHTMLText: 机构登陆acm.org失败！")
        elif url.find("ieeexplore.ieee.org") != -1:
            r = requests.get(url, timeout=60, verify=False, headers=headers)
            if r.text.find("SHENZHEN UNIVERSITY") == -1:
                print("getHTMLText: 机构登陆ieeexplore.ieee.org失败！")
        else:
            r = requests.get(url, timeout=60, verify=False)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except Exception as ex:
        print("getHTMLText: failed:%s" % ex)
        raise Exception("getHTMLText error!")


def get_paper_name(title):
    '''将论文标题修改为合法命名格式
    '''
    for c in list(replace_char.keys()):
        title = title.replace(c, replace_char[c])  # 将标题中的冒号改为-
    return title

def download_one_paper(title, url):
    '''获得下载url，和论文名字（根据论文名字关键词筛选），下载单篇论文
        :param url: 
        :param year: 出版年份
        :param typ: ccf认证类别
        :param conf: 会议名
    '''
    # if url.find('.pdf') == -1:
    #     site = valid_site[conf]
    #     headers["Cookie"] = cookie[site]
    #     headers["Connection"] = "close"

    # html = getHTMLText(url)
    papername = get_paper_name(title)
    pdf_url = url

    get_paper(url=pdf_url, folder=directory,filename=papername + '.pdf')


if __name__ == "__main__":
    # print(len('https://link.springer.com/content/pdf/'))
    url = 'https://dl.acm.org/doi/10.1145/3299869.3319891'
    year = '2019'
    type = 'A'
    conf = 'SIGMOD'
    # download_one_paper(url, year, type, conf)
    # download_one_paper('https://link.springer.com/article/10.1007/s00778-019-00568-7', '2020', 'A', 'VLDB')

    # download_one_paper('https://ieeexplore.ieee.org/document/9155359', '2020', 'A', 'INFOCOM') # failure

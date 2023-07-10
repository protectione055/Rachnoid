'''
Author: YourName
Date: 2022-06-15 21:29:27
LastEditTime: 2022-08-01 18:55:40
LastEditors: YourName
Description: 
FilePath: \download_paper\download_papers.py
版权声明
'''
# from asyncio import FastChildWatcher
import requests
import os
from bs4 import BeautifulSoup
import time
import json
# 本地导入
from download_one_paper import getHTMLText, download_one_paper
# from download_one_paper import *
import random

requests.adapters.DEFAULT_RETRIES = 10


def get_paper_url_list(html):
    '''获取所有论文的下载地址
    '''
    paper_url_list = {}

    soup = BeautifulSoup(html, 'html.parser')

    # 获取论文信息
    boxes = soup.find_all(attrs={'class': 'shadow-app rounded-[10px] transition-all duration-300 p-[16px] hover:shadow-app-hover w-full min-h-[245px] h-full hover:cursor-pointer'})
    for box in boxes:
        # 获取title
        title = box.find(attrs={'class': 'text-grey-5 group-hover:text-primary-1 transition-all duration-300'}).getText()
        print("获取到title: " + title)

        # 获取下载链接
        url_pdf = box.find(attrs={"class": "flex flex-row justify-end space-x-2"}).a['href']
        print("获取到url: " + url_pdf)

        # 将title和url添加到返回结果
        paper_url_list[title] = url_pdf

    # for content in lists:
    #     url = content.contents[0].get('href')

    return paper_url_list


if __name__ == "__main__":
    conf_list = []
    task_list = []
    # 关闭多余的http连接
    s = requests.session()
    s.keep_alive = False

    with open("config.json", 'r', encoding='utf-8') as json_file:
        config = json.load(json_file)
        globals().update(config["config2"])

    # snapshot = {}
    failed_list = []
    # try:
        # tmpf = open("snapshot.json", 'w+')
        # snapshot = json.load(tmpf)
        # from_year = snapshot['from_year']
        # task_list = snapshot['task_list']
        # if from_year in ['failed_url'].keys():
        #     failed_list = snapshot['failed_url'][from_year]
    # except Exception as ex:
    #     from_year = year
    #     snapshot['failed_url'] = {}
    #     print(ex)
    #     print("没有找到快照数据")

    # for y in range(int(from_year), int(until)-1, -1):
        # conf_url = url + str(y) + ".html"  # 获取会议的网站
    conf_url = url
    print("Crawling url: %s" % conf_url)
    # 获取爬取的主页
    html = getHTMLText(conf_url)

    if len(task_list) == 0:
        # 获取所有论文的下载地址，以title-url的形式返回结果
        paper_url_list = get_paper_url_list(html)  # 
    # print(paper_url_list)

    totnum_list = len(paper_url_list)
    i = 0
    failed_count = 0
    for title, url_pdf in paper_url_list.items():
        # 用来观察进度
        print('dealing with %d/%d=%f%%, failed: %d\n' % (i + 1, totnum_list,
                100.0 * (i + 1) / totnum_list, failed_count))  

        # paper_url= 'https://doi.org/10.1145/3299869.3314037'
        try:
            download_one_paper(title, url_pdf)
            i += 1
        except Exception as ex:
            failed_list.append(url_pdf)
            failed_count += 1
            print("Failed to download: ")
            print(ex)

        time.sleep(1+random.random())
    
    print("failed_list", failed_list)

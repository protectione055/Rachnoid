from collector.dblp_collector import DblpCollector
import os


def create_spider(url, type):
    if type == "dblp":
        return DblpCollector(url)


conf_name = "SIGMOD 2023"
url = "https://dblp.uni-trier.de/db/conf/sigmod/sigmod2023c.html"

if not os.path.exists(conf_name):
	os.mkdir(conf_name)
os.chdir(conf_name)

spider = create_spider(url, "dblp")
spider.fetch_papers()
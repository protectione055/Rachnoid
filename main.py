from collector import DblpCollector
import os


conf_name = "SIGMOD 2023"
url = "https://dblp.uni-trier.de/db/journals/pacmmod/pacmmod1.html#nr1"

if not os.path.exists(conf_name):
	os.mkdir(conf_name)
os.chdir(conf_name)

try:
	spider = DblpCollector(url)
	spider.fetch_papers()
except Exception as ex:
	print("fetch_papers: failed:%s" % ex)
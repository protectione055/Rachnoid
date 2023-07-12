from abc import ABC, abstractmethod

class AbstractDownloader(ABC):
	def __init__(self, url):
		self.url = url

	def get_valid_filename(self, filename):
		filename = filename.replace(": ", " - " ).replace("/", "-").replace("*", "-star").replace("?", "").replace("\"", " ").replace("<", "[").replace(">", "]").replace("|", "-")
		return filename

	def save_content_to_file(self, path, content):
		try:
			with open(path, "wb") as f:
				f.write(content)
				f.close()
		except Exception as ex:
			print("save_content_to_file: failed:%s" % ex)
			raise Exception("save_content_to_file error: " + path)
	
	@abstractmethod
	def download_paper_from_url(self, directory, name, url):
		pass
	
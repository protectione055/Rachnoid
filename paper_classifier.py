import os
import difflib

class PaperClassfier():
    def __init__(self, src_dir, tar_dir, index_file):
        self.src_dir = src_dir
        self.tar_dir = tar_dir
        self.idx_file = index_file
        self.reverse_index = {}
    
    def __get_valid_filename(self, filename):
        filename = filename.replace(": ", " - " ).replace("/", "-").replace("*", "-star").replace("?", "").replace("\"", " ").replace("<", "[").replace(">", "]").replace("|", "-")
        return filename
        
    def classfy(self):
        with open(self.idx_file, 'r') as f:
            lines = f.readlines()
            session = ''
            for line in lines:
                if line == '\n':
                    continue
                line = line.strip('\n').strip(' ')
                if line.startswith('Session'):
                    session = self.__get_valid_filename(line)
                    if not os.path.exists(os.path.join(self.tar_dir, session)):
                         os.mkdir(os.path.join(self.tar_dir, session))
                else:
                    paper = self.__get_valid_filename(line) + '.pdf'
                    self.reverse_index[paper] = session
                    if os.path.exists(os.path.join(self.src_dir, paper)):
                        os.rename(os.path.join(self.src_dir, paper), os.path.join(self.tar_dir, session, paper))
                    # else:
                        # print('[file not found] %s ' % paper)
    
    # 处理剩下的文件
    def process_left(self):
        # 遍历目录下所有文件，不检查子目录
        for file in os.listdir(self.src_dir):
            print("Checking %s" % file)
            # 在反向索引中查找最相似的文件名
            thred_ratio = 0.8
            max_ratio = 0
            max_key = ''
            for key in self.reverse_index.keys():
                ratio = difflib.SequenceMatcher(None, file, key).ratio()
                if ratio > max_ratio:
                    max_ratio = ratio
                    max_key = key
                if ratio > thred_ratio:
                    session_name = self.reverse_index[key]
                    os.rename(os.path.join(self.src_dir, file), os.path.join(self.tar_dir, session_name, file))
            print(max_ratio, max_key)


if __name__ == "__main__":
    src_dir = '.\\SIGMOD 2023'
    tar_dir = '.\\SIGMOD 2023'
    index_file = '.\\sigmod2023-industry.txt'
    classifier = PaperClassfier(src_dir, tar_dir, index_file)
    classifier.classfy()
    classifier.process_left()
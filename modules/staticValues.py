import configparser
parser = configparser.ConfigParser()
parser.read("conf.ini")

class pageObj:
    def __init__(self):
        self.postdata = None
        self.getdata = None
        self.sess = None
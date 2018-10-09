import configparser
import os

parser = configparser.ConfigParser()
conf_file_name = "conf.ini"



class pageObj:
    def __init__(self):
        self.postdata = None
        self.getdata = None
        self.sess = None

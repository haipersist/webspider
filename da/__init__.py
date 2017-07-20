
from webspider.baseclass.database import Database
from utils.mylogger import MyLogger



class BaseJob(object):

    def __init__(self):
        self.db = Database()
        self.logger = MyLogger('dailyjob').logger





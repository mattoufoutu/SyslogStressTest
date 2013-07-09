__author__ = 'pyt'

from random import choice

class LogEvent(object):
    '''
    classdocs
    '''
    _instance = None
    def __init__(self,path='sample/bluecoat.log'):
        '''
        Constructor
        '''
        self.list=[]
        self.path=path
        with open(self.path,'r') as fr:
            for log in fr:
                self.list.append(log)

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(LogEvent, cls).__new__(
                cls, *args, **kwargs)
        return cls._instance

    def rand(self):
        return choice(self.list)
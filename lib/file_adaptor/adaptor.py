from lib.parsing.parser import Parser
class FileAdaptor:
    def __init__(self,parser: Parser):
        self.parser = parser

    def convert(self,filename):
        raise NotImplementedError
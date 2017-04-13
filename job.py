from bs4 import BeautifulSoup

class Job:
    def __init__(self,outputPath):
        self.outputPath = outputPath

    def do(self,contents):
        print('some job done')
        html = BeautifulSoup(contents)
        

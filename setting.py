import re

class Settings:
    _settings={'settingPath':'./setting.txt', 'url':'https://arxiv.org', 'keyword':'','outputPath':'./OUTPUT', 'resultPath':'./OUTPUT/result.md', 'isdownload':0}
    def addKey(self,key,value):
        self._settings[key]=value
    def getValue(self,key):
        return self._settings[key]
    def updKey(self,key,value):
        pass
    def __init__(self,path):
        pattern=r"^//"
        with open(path,'r') as f:
            settings = f.read()
            settings = settings.split('\n')
            for line in settings:
                if re.search(pattern,line):
                    continue
                line=line.split(' ')
                self._settings[line[0]]=line[2].replace('\'','')
import threading
import re
import fileOperator as fo
from setting import Settings

from html.parser import HTMLParser
from urllib.request import urlopen
from urllib import parse

# Const Vars
settingPath = './setting.txt'

class linksFinder(HTMLParser):
    def __init__(self,baseUrl):
        super().__init__()
        self.base_url = baseUrl
        self.links = set()
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for (attribute, value) in attrs:
                if attribute == 'href':
                    url = parse.urljoin(self.base_url, value)
                    self.links.add(url)

class Spider:
    baseUrl = ''
    todo = set()
    done = set()
    def __init__(self,baseUrl,temPath):
        Spider.baseUrl = baseUrl
        todoPath = temPath + '/todolist.txt'
        donePath = temPath + '/donelist.txt'
        fo.createDir(temPath)
        fo.createFile(todoPath)
        fo.createFile(donePath)
        Sipder.todo = set(fo.file2list(todoPath))
        Spider.done = set(fo.file2list(donePath))
        self.crawl('1st',Spider.baseUrl)

    @staticmethod
    def gatherURL(url):
        html=''
        response = urlopen(url)
        if 'text/html' in response.getheader('Content-Type'):
            html=response.read()
            html=html.decode('utf-8')
        res = linksFinder(Spider.baseUrl)
        res.feed(html)
        return res.links, html

    @staticmethod
    def crawl(name,url):
        if url not in Spider.done:
            newUrl,contents=Spider.gatherURL(url)
            for iterm in newUrl:
                if (iterm not in Spider.done) and (iterm not in Spider.todo):
                    Spider.todo.add(iterm)
            print(Spider.todo)
            Spider.todo.remove(url)
            Spider.done.add(url)
            list2file(todoPath,list(Spider.todo))
            list2file(donePath,list(Spider.done))


if __name__ == "__main__":
    settings = Settings(settingPath)
    baseUrl = settings.getValue('URL')
    temPath = settings.getValue('outputPath')
    spider = Spider(baseUrl,temPath)


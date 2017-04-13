from html.parser import HTMLParser
from urllib.request import urlopen
from urllib import parse
import fileOperator as fo

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
    todoPath = ''
    donePath = ''
    baseUrl = ''
    todo = set()
    done = set()
    domain = ''
    def __init__(self,baseUrl,temPath,job):
        Spider.baseUrl = baseUrl
        Spider.todoPath = temPath + '/todolist.txt'
        Spider.donePath = temPath + '/donelist.txt'
        Spider.domain = baseUrl
        Spider.job = job
        fo.createDir(temPath)
        fo.createFile(Spider.todoPath)
        fo.createFile(Spider.donePath)
        Spider.todo = set(fo.file2list(Spider.todoPath))
        Spider.todo.add(Spider.baseUrl)
        Spider.done = set(fo.file2list(Spider.donePath))
        print('Initizing Spider')
        self.crawl('1st',Spider.baseUrl)

    @staticmethod
    def gatherURL(url):
        html=''
        try:
            response = urlopen(url)
            if 'text/html' in response.getheader('Content-Type'):
                html=response.read()
                html=html.decode('utf-8')
            res = linksFinder(Spider.baseUrl)
            res.feed(html)
            return res.links, html
        except Exception as e:
            print(str(e))
            return set(),html


    @staticmethod
    def crawl(name,url):
        print("Spider "+name+"is now crawling "+url)
        if url not in Spider.done:
            newUrl,contents=Spider.gatherURL(url)
            for iterm in newUrl:
                if (iterm not in Spider.done) and (iterm not in Spider.todo) and (Spider.domain in iterm):
                    Spider.todo.add(iterm)
            Spider.todo.remove(url)
            Spider.done.add(url)
            Spider.job(contents)
            fo.list2file(Spider.todoPath,list(Spider.todo))
            fo.list2file(Spider.donePath,list(Spider.done))

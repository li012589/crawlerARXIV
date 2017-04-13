import threading
import re
import fileOperator as fo
from setting import Settings
from spider import Spider
from job import job
from queue import Queue

# Const Vars
settingPath = './setting.txt'
MaxThreading = 1
queue = Queue()

def work():
    while True:
        url = queue.get()
        spider.crawl(threading.current_thread().name, url)
        queue.task_done()

def create_jobs():
    for link in fo.file2list('./OUTPUT/todolist.txt'):
        queue.put(link)
    queue.join()
    crawl()
def crawl():
    queued_links = fo.file2list('./OUTPUT/todolist.txt')
    if len(queued_links) > 0:
        print(str(len(queued_links)) + ' links in the queue')
        create_jobs()

def updateTask(pathtoFile):
    while True:
        tasks = fo.file2list(pathtoFile)
        for task in tasks:
            queue.put(task)
        queue.join()

def threadingCrawl():
    for works in range(MaxThreading):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()

if __name__ == "__main__":
    settings = Settings(settingPath)
    baseUrl = settings.getValue('URL')
    temPath = settings.getValue('outputPath')
    queuePath = settings.getValue('outputPath') + '/todolist.txt'
    spider = Spider(baseUrl,temPath,job)
    create_workers()
    #    crawl()
    updateTask(queuePath)
import threading
import re
from shutil import rmtree
import fileOperator as fo
from setting import Settings
from spider import Spider
from job import job
from queue import Queue

# Const Vars
queue = Queue()
settingPath = './setting.txt'

def work():
    while True:
        url = queue.get()
        spider.crawl(threading.current_thread().name, url)
        queue.task_done()

def updateTask(pathtoFile):
    while True:
        tasks = fo.file2list(pathtoFile)
        for task in tasks:
            queue.put(task)
        queue.join()

def threadingCrawl(maxThread):
    for works in range(maxThread):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()

if __name__ == "__main__":
    settings = Settings(settingPath)
    baseUrl = settings.getValue('URL')
    temPath = settings.getValue('outputPath')
    queuePath = settings.getValue('outputPath') + '/todolist.txt'
    maxThread = int(settings.getValue('ThreadingMaxNum'))
    isClear = int(settings.getValue('isClear'))
    sleepTime = int(settings.getValue('SleepTime'))
    if isClear == 1:
        try:
            rmtree(temPath)
        except:
            print('Not find temporary folder')
        else:
            print('Temporary folder removed! (Can\'t continue after break, change at setting.txt)')

    spider = Spider(baseUrl,temPath,job)
    threadingCrawl(maxThread)
    updateTask(queuePath)
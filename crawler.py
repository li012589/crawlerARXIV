import threading
import re
from shutil import rmtree
from time import sleep
import fileOperator as fo
from setting import Settings
from spider import Spider
from job import job
from queue import Queue

# Const Vars
queue = Queue()
settingPath = './setting.txt'

def work(time):
    while True:
        url = queue.get()
        spider.crawl(threading.current_thread().name, url)
        sleep(time)
        queue.task_done()

def updateTask(pathtoFile):
    while True:
        tasks = fo.file2list(pathtoFile)
        for task in tasks:
            queue.put(task)
        queue.join()

def threadingCrawl(maxThread,sleepTime):
    for works in range(maxThread):
        t = threading.Thread(target=work,args=(sleepTime,))
        t.daemon = True
        t.start()

if __name__ == "__main__":
    settings = Settings(settingPath)
    baseUrl = settings.getValue('URL')
    temPath = settings.getValue('outputPath')
    queuePath = settings.getValue('outputPath') + '/todolist.txt'
    maxThread = int(settings.getValue('ThreadingMaxNum'))
    isClear = int(settings.getValue('isClear'))
    sleepTime = float(settings.getValue('SleepTime'))
    passFeature = settings.getValue('WhatToPass')
    if isClear == 1:
        try:
            rmtree(temPath)
        except:
            print('Not find temporary folder')
        else:
            print('Temporary folder removed! (Can\'t continue after break, change at setting.txt)')

    spider = Spider(baseUrl,temPath,passFeature,job)
    threadingCrawl(maxThread,sleepTime)
    updateTask(queuePath)
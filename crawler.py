import threading
import re
import fileOperator as fo
from setting import Settings
from spider import Spider
from job import job

# Const Vars
settingPath = './setting.txt'

if __name__ == "__main__":
    settings = Settings(settingPath)
    baseUrl = settings.getValue('URL')
    temPath = settings.getValue('outputPath')
    spider = Spider(baseUrl,temPath,job)

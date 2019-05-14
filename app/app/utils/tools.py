# -*-  coding: utf-8 -*-

import re
import os
import urllib
import string
import random
from twisted.internet import reactor
from multiprocessing import Queue, Process
from scrapy.crawler import CrawlerRunner, CrawlerProcess
from scrapy.utils.project import get_project_settings

# 删除 HTML 所有标签
def remove_all_tags(str):
  r = re.compile(r'<.*?>')
  str = r.sub('', str)
  return str.replace(u'\u3000', '')

# 随机生成字符串
def randomString(len = 10):
  letters = string.ascii_letters
  return ''.join(random.choice(letters) for i in range(len))

# 下载文件
def download_file(url):
  path = os.path.abspath(os.curdir)
  filename = randomString()
  dldir = "%s/files" % (path) # 下载目录
  if not os.path.exists(dldir):
    os.makedirs(dldir)
  dlfile = "%s/%s" % (dldir, filename)

  urllib.urlretrieve(url, dlfile)
  return dlfile

def processFunc(q, spider):
  try:
    runner = CrawlerProcess(get_project_settings())
    runner.crawl(spider)
    runner.start()
    q.put(None)
  except Exception as e: 
    q.put(e)

def runSpider(spider):

  q = Queue()
  p = Process(target=processFunc, args=(q, spider, ))
  p.start()
  result = q.get()
  p.join()

  if result is not None:
    raise result




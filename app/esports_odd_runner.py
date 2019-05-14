# -*- coding: utf-8 -*-

from app.spiders.ouresports_odd import OuresportsOdd
import time
from app.utils.tools import runSpider

if __name__ == "__main__":
  print u"自动运行电竞赛事数据脚本"



  while True:
    
    # 抓取电竞数据
    runSpider(OuresportsOdd)

    # 休眠一段时间后 再次执行抓取
    time.sleep(60 * 1) # 1分钟执行一次

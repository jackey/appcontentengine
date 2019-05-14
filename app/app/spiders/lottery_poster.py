# -*- coding: utf-8 -*-

import scrapy
import re
from app.items import LotteryPoster

class lottery_poster(scrapy.Spider):

  name = 'lottery_poster'
  allow_domains = ['www.china-lottery.net']

  def start_requests(self):
    url = 'http://www.china-lottery.net/'
    yield scrapy.Request(url=url, callback=self.parse_poster)

  def parse_poster(self, response):
    styles = response.css('.largeBanner').xpath('@style').getall()

    # 解析图片地址
    for style in styles:
      matched = re.search(r'\(([^\)]+)\)', style)
      if matched is not None:
        src = matched.group(1)
        self.logger.debug(u"图片地址: %s" % src)

        # 图片
        yield LotteryPoster(
          src=src,
          source=response.url
        )
        
  

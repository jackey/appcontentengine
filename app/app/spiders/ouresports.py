# -*- coding:  utf-8 -*-

# 电竞大师
# http://www.ouresports.com
# 抓取电竞新闻资讯

import scrapy
import json
from app.items import EsportNews

class Ouresports(scrapy.Spider):

  name = "ouresports"
  allowed_domains = ["api.ouresports.com"]

  pager_url = "http://api.ouresports.com/api/news"
  detail_url = "http://api.ouresports.com/web/news"

  items = {}

  # 开启请求
  def start_requests(self):

    yield scrapy.Request(url="%s?page=1&category=all&game_id=1" % self.pager_url, callback=self.parse_news_page, meta={
      "start": True
    })


  # 解析分页页面
  def parse_news_page(self, response):
    data = json.loads(response.body_as_unicode())
    is_start = response.meta["start"] if "start" in response.meta else False
    # 起始分页
    if is_start:
      # 总页码
      meta = data["meta"]
      total_page = meta['total_count'] / meta['per'] if meta['total_count'] % meta['per'] == 0 else int(meta['total_count'] / meta['per']) + 1

      # 1 - total_page 分页
      for i in range(0, total_page):
        yield scrapy.Request(url="%s?page=%d&category=all&game_id=1" % (self.pager_url, i), callback=self.parse_news_page )

    # 解析分页项目
    else:
      for news in data["news"]:
        model = EsportNews()
        model['author'] = news['author']
        model['cover_image'] = news['cover_image']
        model['created'] = news['created_at']
        model['title'] = news['title']
        model['id'] = news['id']
        self.items[model['id']] = model
        yield scrapy.Request(url="%s/%s" % (self.detail_url, model['id']), callback=self.parse_detail_page)

  # 解析详情页面  
  def parse_detail_page(self, response):
    data = json.loads(response.body_as_unicode())

    model = self.items[data['news']['id']]
    model['content'] = data['news']['content']
    
    yield model
      
       
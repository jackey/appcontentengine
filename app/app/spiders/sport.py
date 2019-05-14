# -*- coding: utf-8 -*-

import scrapy
import re

from app.items import SportArticle

# 体育新闻爬虫
# https://www.521530.com/
class Sport(scrapy.Spider):

  name = 'sport'
  allow_domain=['www.521530.com']

  def start_requests(self):
    url = "https://www.521530.com/"

    yield scrapy.Request(url=url, callback=self.parse)

  def parse(self, response):
    
    # 推荐
    links = response.css('ul.ilist_c li a').xpath('@href').getall()
    for link in links:
      yield scrapy.Request(url=response.urljoin(link), callback=self.parseDetail, meta={
        "group": u"热门推荐"
      })

    # 足球新闻
    link1 = response.css('.box2 .box2_l dl dt a').xpath('@href').get()
    yield scrapy.Request(url=response.urljoin(link1), callback=self.parseDetail, meta={
      "group": u"足球新闻"
    })

    links = response.css('.box2 .box2_l ul li a').xpath('@href').getall()
    for link in links:
      yield scrapy.Request(url=response.urljoin(link), callback=self.parseDetail, meta={
        "group": u"足球新闻"
      })

    #篮球新闻
    link1 = response.css('.box2 .box2_c dl dt a').xpath('@href').get()
    yield scrapy.Request(url=response.urljoin(link1), callback=self.parseDetail, meta={
      "group": u"篮球新闻"
    })

    links = response.css('.box2 .box2_c ul li a').xpath('@href').getall()
    for link in links:
      yield scrapy.Request(url=response.urljoin(link), callback=self.parseDetail, meta={
        "group": u"篮球新闻"
      })
      

    #综合新闻
    link1 = response.css('.box2 .box2_c dl dt a').xpath('@href').get()
    yield scrapy.Request(url=response.urljoin(link1), callback=self.parseDetail, meta={
      "group": u"综合新闻"
    })

    links = response.css('.box2 .box2_c ul li a').xpath('@href').getall()
    for link in links:
      yield scrapy.Request(url=response.urljoin(link), callback=self.parseDetail, meta={
        "group": u"综合新闻"
      })

    # NBA 赛事
    # NBA 东部赛事
    links = response.css('.box3 #div2 dl dt a').xpath('@href').getall()
    for link in links:
      yield scrapy.Request(url=response.urljoin(link), callback=self.parseDetail, meta={
        "group": u"NBA赛事",
        "group_ext1": u"东部赛事",
      })

    # NBA 西部赛事
    links = response.css('.box3 #div1 dl dt a').xpath('@href').getall()
    for link in links:
      yield scrapy.Request(url=response.urljoin(link), callback=self.parseDetail, meta={
        "group": u"NBA赛事",
        "group_ext1": u"西部赛事",
      })

    # 赛事预测
    links = response.css('.box4 .box2_r li a').xpath('@href').getall()
    for link in links:
      yield scrapy.Request(url=response.urljoin(link), callback=self.parseDetail, meta={
        "group": u"赛事预测",
      })

    #赛事预测
    #足球分析
    links = response.css('.box4 .box2_l li a').xpath('@href').getall()
    for link in links:
      yield scrapy.Request(url=response.urljoin(link), callback=self.parseDetail, meta={
        "group": u"赛事预测",
        "group_ext1": u"足球分析",
      })

    links = response.css('.box4 .box2_c li a').xpath('@href').getall()
    for link in links:
      yield scrapy.Request(url=response.urljoin(link), callback=self.parseDetail, meta={
        "group": u"赛事预测",
        "group_ext1": u"篮球分析",
      })

  def parseDetail(self, response):
    title = response.css('.title h1').xpath('text()').get()
    resource = response.css('.resource').xpath('text()').get()
    parts = resource.split()
    author = parts[1].split(u'：')[1]
    source = parts[0].split(u'：')[1]

    resource = response.css('.resource').get()
    matched = re.search(ur"发布时间：([\w\s\-\:]+)", resource)

    # 发布时间
    publish_date = '2019-02-27 13:00:00'
    if matched is not None:
      publish_date = matched.group(1)
    
    
    short_des = response.css('.des').xpath('text()').get()
    content = response.css('.content table tr td ').get()

    #替换图片 地址
    allimgs = response.css('.content table tr td img').xpath('@src').getall()
    if len(allimgs) > 0:
      poster = response.urljoin(allimgs[0])
    else:
      poster = ''
    for img in allimgs:
      content = content.replace(img, response.urljoin(img))

    yield SportArticle(
      title=title, 
      author=author,
      source=source,
      group=response.meta['group'],
      type=u"体育资讯",
      voted=0,
      publish_date=publish_date,
      short_desc=short_des,
      content=content,
      poster=poster,
      group_ext1= response.meta['group_ext1'] if 'group_ext1' in response.meta else ''
    )
    
    


  
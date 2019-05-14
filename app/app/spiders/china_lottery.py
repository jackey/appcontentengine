# -*- coding: utf-8 -*-
import scrapy
import md5
from app.utils.tools import remove_all_tags

from app.items import Article

# 中国彩票网站 
# 1. 热点推荐
# 2. 投注攻略
# 3. 新闻资讯
# 4. 彩票文化
class ChinaLotterySpider(scrapy.Spider):
    name = 'china-lottery'
    allowed_domains = ['www.china-lottery.net']
    jq_url = 'http://www.china-lottery.net/news/zhuanjia/'

    def start_requests(self):
        urls = ['http://www.china-lottery.net/']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        # 热点推荐 =================  开始 =================================
        list_b = response.css("div.list_b")
        # h2 
        link = list_b.css('h2 a').xpath('@href').get()
        self.logger.debug(u"抓取h2 %s" %( link ))
        yield scrapy.Request(url=response.urljoin(link), callback=self.parseDetail, meta={
            'group': u'热点推荐',
            'type': u'行业资讯'
        })

        # h4 
        link = list_b.css('h4 a').xpath('@href').get()
        self.logger.debug(u"抓取h2 %s" %( link))
        yield scrapy.Request(url=response.urljoin(link), callback=self.parseDetail, meta={
            'group': u'热点推荐',
            'type': u'行业资讯'
        })

        # h5 
        links = list_b.css('h5 a').xpath('@href').getall()
        for link in links:
            self.logger.debug(u"抓取h2 %s" %( link))
            yield scrapy.Request(url=response.urljoin(link), callback=self.parseDetail, meta={
            'group': u'热点推荐',
            'type': u'行业资讯'
        })

        # li列表
        links = list_b.css('ul.f16 li a').xpath('@href').getall()
        for link in links:
            yield scrapy.Request(url=response.urljoin(link), callback=self.parseDetail, meta={
            'group': u'热点推荐',
            'type': u'行业资讯'
        })
        # 热点推荐 =================  结束 =================================
        
        # 投注攻略 & 资讯 =================  开始 =================================
        links = response.css('.col_320 .list-s ul li a').xpath('@href').getall()
        self.logger.debug("抓取投注攻略 & 资讯  ")
        self.logger.debug(links)
        for link in links:
            yield scrapy.Request(url=response.urljoin(link), callback=self.parseDetail, meta={
                'group': u'投注攻略',
                'type': u'行业资讯'
            })
        # 投注攻略 & 资讯 =================  结束 =================================
        
        # 彩票文化 =================  开始 ========================================
        links = response.css('.list-s1  .f14 li a ').xpath('@href').getall()
        self.logger.debug("抓取彩票文化 ")
        self.logger.debug(links)
        for link in links:
            yield scrapy.Request(url=response.urljoin(link), callback=self.parseDetail, meta={
                'group': u'彩票文化',
                'type': u'行业资讯'
            })
        # 彩票文化 =================  结束 ========================================

        # 抓取投注技巧内容
        yield scrapy.Request(url=self.jq_url, callback=self.parseJqPage)

    # 解析技巧主页
    def parseJqPage(self, response):
        self.logger.debug("解析专家技巧页面")
        links = response.css('.list1 li a ').xpath('@href').getall()
        for link in links:
            yield scrapy.Request(url=response.urljoin(link), callback=self.parseDetail, meta={
                'group': u'投注攻略',
                'type': u'行业资讯'
            })


    # 解析新闻内容
    def parseDetail(self, response):
        title = response.css('h1.title::text').get()
        group = response.meta['group']

        # 不是一个标准得新闻内容
        if title is None:
            return

        self.logger.debug(u"抓取内容: %s" % title)
        date = response.css('span.pubtime::text').get()
        type = response.meta['type']

        # 计算内容唯一ID
        hasher = md5.new()
        hasher.update(title.encode('utf-8'))
        uuid = hasher.hexdigest()

        source = self.name

        # 解析内容中图片地址
        imgs = response.css('.content img').xpath('@src').getall()
        content = response.css('.content').get()
        for img in imgs:
            absimg = response.urljoin(img)
            content = content.replace(img, absimg)
        
        yield Article(title=title, subtitle=remove_all_tags(content),  content=content, source=source, uuid=uuid, type=type, date=date, group=group)


        

        



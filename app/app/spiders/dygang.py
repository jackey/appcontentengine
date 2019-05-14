# -*- coding: utf-8 -*-
import scrapy

from app.items import Movie
import re
import md5


class DygangSpider(scrapy.Spider):
    name = 'dygang'
    allowed_domains = ['www.dygang.net']

    def start_requests(self):
        start_urls = ['http://www.dygang.net']
        for url in start_urls:
            yield scrapy.Request(url=url,  callback=self.parse_index_page)

    # 解析首页
    def parse_index_page(self, response):
        # 导航抓取
        urls = response.css('.bg-fleet a').xpath('@href').getall()
        for url in urls:
            # 首页忽略
            if url == u"/":
                continue
            # 不要电影专题
            if 'dyzt' in url:
                continue
            self.logger.debug(u"抓取主页导航  %s" % url)
            yield scrapy.Request(url=response.urljoin(url), callback=self.parse_list_page, meta={
                'recursive': True
            })

    # 解析列表页面
    def parse_list_page(self, response):

        recursive = response.meta['recursive']

        # 电影页面链接
        detail_links = response.css('.classlinkclass').xpath('@href').getall()
        for link in detail_links:
            if link == u"/":
                continue
            yield scrapy.Request(url=link, callback=self.parse_detail_page)
        
        # 递归查询分页页面
        if recursive:
            pager_links = response.xpath('//td[a[@title="Total record"]]/a/@href').getall()
            for link in pager_links:
                yield scrapy.Request(url=link, callback=self.parse_list_page, meta={
                    "recursive": False
                })

    # 解析详情页面
    def parse_detail_page(self, response):

        # 标题
        title = response.xpath('/html/body/table[6]/tbody/tr/td/table/tbody/tr/td/table[3]/tr[1]/td[2]/text()').get()

        # 小图标
        avatar = response.xpath('/html/body/table[6]/tbody/tr/td/table/tbody/tr/td/table[3]/tr[1]/td//img/@src').get()
        
        # 解析发布日期
        date = response.xpath('/html/body/table[6]/tbody/tr/td/table/tbody/tr/td/table[3]/tr[2]/td/text()').get()
        if date is not None:
            matched = re.search(r'[0-9\-]+', date.encode('utf-8'))
            if matched is not None:
                date = matched.group()
        if date is None:
            date = '2019-02-12'

        short_desc = response.xpath('/html/body/table[6]/tbody/tr/td/table/tbody/tr/td/table[3]/tr[3]/td/text()').get()

        # 解析内容
        pcontainer = response.xpath('/html/body/table[6]/tbody/tr/td/table/tbody/tr/td/table[4]/tbody/tr/td/table/tr/td[1]')
        
        # 大海报
        self.logger.debug("电影 %s => %s" % (title.encode('utf-8') , response.url ) )
        poster = pcontainer.xpath('p[1]/img/@src').get()
        if poster is None:
            poster = ''

        # 电影内容块儿 - 正则分析
        content = pcontainer.get()
        # 去掉html所有的空白符
        content = re.sub(r'[\n\r]+', '', content) 
        
        matched = re.search(ur"◎译　　名([^<]+)", content)
        if matched is not None:
            tr_title = matched.group(1)
        else:
            tr_title = ''

        matched = re.search(ur'◎片　　名([^<]+)', content)
        if matched is not None:
            title = matched.group(1)
        else:
            title = ''
        
        self.logger.debug("标题")
        self.logger.debug(title)

        matched = re.search(ur'◎年　　代([^<]+)', content)
        if matched is not None:
            year = matched.group(1)
        else:
            year = ''

        matched = re.search(ur'◎产　　地([^<]+)', content)
        if matched is not None:
            country = matched.group(1)
        else:
            country = ''

        matched = re.search(ur'◎地　　区([^<]+)', content)
        if matched is not None:
            country = matched.group(1)
        
        matched = re.search(ur'◎类　　别(.+<\/a>)', content)
        if matched is not None:
            group = matched.group(1)
            groups = re.findall('<a[^>]+>([^<]+)<\/a>', group)
            if groups is not None:
                types = []
                for name in groups:
                    if len(name) > 5 or name ==  u'迅雷' or u'电影' in name:
                        continue
                    types.append(name)
                group = ','.join(types)
            else:
                self.logger.debug("没有匹配到类别")
        else:
            group = ''
        
        self.logger.info("匹配到得类别为 %s " % group.encode('utf-8') )
        
        matched = re.search(ur'◎语　　言([^<]+)', content)
        if matched is not None:
            language = matched.group(1)
        else:
            language = ''

        matched = re.search(ur'◎字　　幕([^<]+)', content)
        if matched is not None:
            subtitles = matched.group(1)
        else:
            subtitles = ''

        matched = re.search(ur'◎上映日期([^<]+)', content)
        if matched is not None:
            release_date = matched.group(1)
        else:
            release_date = ''
        self.logger.debug("发布日期")
        self.logger.debug(release_date.encode('utf-8'))

        matched = re.search(ur'◎IMDb评分([^<]+)', content)
        if matched is not None:
            imdb_score = matched.group(1)
        else:
            imdb_score = ''

        matched = re.search(ur'◎豆瓣评分([^<]+)', content)
        if matched is not None:
            douban_score = matched.group(1)
        else:
            douban_score = ''

        matched = re.search(ur'◎片　　长([^<]+)', content)
        if matched is not None:
            duration = matched.group(1)
        else:
            duration = ''
        
        matched = re.search(ur'◎导　　演([^<]+)', content)
        if matched is not None:
            director = matched.group(1)
        else:
            director = ''

        matched = re.search(ur'◎编　　剧([^<]+)', content)
        if matched is not None:
            screenwriter = matched.group(1)
        else:
            screenwriter = ''
        
        matched = re.search(ur'◎主　　演(.+?)</p>', content)
        if matched is not None:
            actor = matched.group(1)
            actor = re.sub(r'<br\/>|<br>', ",", actor)
        else:
            actor = ''
        
        matched = re.search(ur'◎简　　介(.+?)</p>', content)
        self.logger.debug(u"简介")
        if matched is not None:
            desc = matched.group(1)
            desc = re.sub(r'<br\/>|<br>', "\r\n", desc)
            desc = re.sub(r'<a[^>].+</a>', '', desc)
        else:
            desc = ''

        # 下载地址
        download_links = pcontainer.xpath('table[1]').get()

        # 频道
        channel = response.xpath('/html/body/table[6]/tbody/tr[1]/td/table/tbody/tr/td/table/tbody/tr/td//a[2]/text()').get()

        hasher = md5.new()
        hasher.update(title.encode('utf-8'))
        uuid = hasher.hexdigest()
        movie = Movie(
            uuid = uuid,
            title=title.strip(),
            tr_title=tr_title.strip(),
            desc=desc.strip(),
            short_desc=short_desc.strip(),
            date=date.strip(),
            type=u'电影影视',
            channel=channel.strip(),
            groups=group.strip(),
            language=language.strip(),
            subtitles=subtitles.strip(),
            release_date=release_date.strip(),
            imdb_score=imdb_score.strip(),
            douban_score=douban_score.strip(),
            duration=duration.strip(),
            director=director.strip(),
            screenwritter=screenwriter.strip(),
            actors=actor.strip(),
            download_links=download_links.strip(),
            poster=poster.strip(),
            avatar=avatar.strip(),
            year=year.strip(),
            country=country.strip()
        )
        yield movie
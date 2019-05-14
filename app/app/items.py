# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class AppItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

# 文章内容
class Article(scrapy.Item):
    title = scrapy.Field()
    subtitle = scrapy.Field()
    content = scrapy.Field()
    date = scrapy.Field(serializer=str)
    group = scrapy.Field() # 内容分组 
    type =  scrapy.Field() # 内容类型 - 资讯
    uuid = scrapy.Field() # 内容得唯一ID - md5(title)
    source = scrapy.Field() # 内容来源

# 电影影视
class Movie(scrapy.Item):
    uuid = scrapy.Field() # UUID
    title= scrapy.Field() # 名称 
    tr_title = scrapy.Field() # 译名
    desc = scrapy.Field() # 简介
    short_desc = scrapy.Field() # 短简介
    date = scrapy.Field() # 上架日期
    type = scrapy.Field() # 内容类型 - 电影
    channel = scrapy.Field() # 电影频道 - 美剧 / 日韩 / 港澳
    groups = scrapy.Field()  # 电影类型 - [剧情, 科幻, 冒险]
    language = scrapy.Field() # 语言
    subtitles = scrapy.Field() # 字幕语言 - [ 英语, 日语 ]
    release_date = scrapy.Field() # 上映时间
    imdb_score = scrapy.Field()  # IMDB 评分
    douban_score = scrapy.Field() # 豆瓣 评分
    duration = scrapy.Field() # 片长 - 1小时30分钟
    director = scrapy.Field() # 导演
    screenwritter = scrapy.Field() # 编剧
    actors = scrapy.Field() # 演员列表 - [aa,bb,cc]
    download_links = scrapy.Field() # HTML 标签
    poster = scrapy.Field() # 海报
    avatar = scrapy.Field() # 电影小头像
    year = scrapy.Field() # 年代
    country = scrapy.Field() # 产地

# 彩票幻灯片
class LotteryPoster(scrapy.Item):
    src = scrapy.Field()
    source = scrapy.Field()

# 体育新闻
class SportArticle(scrapy.Item):
    title = scrapy.Field()
    source = scrapy.Field()
    author = scrapy.Field()
    voted = scrapy.Field()
    publish_date = scrapy.Field()
    short_desc = scrapy.Field()
    content = scrapy.Field()
    poster = scrapy.Field() # 海报
    type = scrapy.Field() # 类型 - 资讯
    group = scrapy.Field() # 分组
    group_ext1 = scrapy.Field() # 扩展分组1

# 电竞资讯
class EsportNews(scrapy.Item):
    title = scrapy.Field()
    author = scrapy.Field()
    cover_image = scrapy.Field()
    created = scrapy.Field()
    content = scrapy.Field()
    id = scrapy.Field()

# 电竞赛事
class EsportComeption(scrapy.Item):
    title = scrapy.Field() # 赛事名字
    platform = scrapy.Field() # 赛事游戏平台

# 电竞战队赛事
class EsportCompetionTeam(scrapy.Item):
    bet_topic_count = scrapy.Field() # 专题数
    game_platform = scrapy.Field() # 游戏平台
    id = scrapy.Field() # 赛事ID
    in_play = scrapy.Field() # 是否滚球
    league_name = scrapy.Field() #赛事名称
    left_team = scrapy.Field() # 主场战队
    right_team = scrapy.Field() # 客场战队
    round = scrapy.Field() # 比赛赛制 B03 三局两胜
    start_time = scrapy.Field() # 比赛开始时间
    status = scrapy.Field() # 状态

# 比赛战队
class EsportTeam(scrapy.Item):
    id = scrapy.Field() 
    logo = scrapy.Field() # Logo
    tag = scrapy.Field() # 简称
    
# 比赛盘口
class EsportPankou(scrapy.Item):
    id = scrapy.Field() # 盘口唯一id
    game_no = scrapy.Field() # 第一回合 0: 全局
    team_competion = scrapy.Field() # 战队赛事
    end_time = scrapy.Field() # 盘口结束时间
    handicap = scrapy.Field() # 让分数
    key = scrapy.Field()  
    kill_count = scrapy.Field() # 击败数
    type = scrapy.Field() # 盘口类型
    topicable_type = scrapy.Field() # 字段未知
    value = scrapy.Field() # 不同的盘口类型 来显示数据
    bet_topics =  scrapy.Field() # 比赛盘口赔率

# 比赛赔率
class EsportPankouOdd(scrapy.Item):
    id = scrapy.Field()
    checkout_status = scrapy.Field() # 结算状态
    in_play = scrapy.Field() # 是否滚球
    left_odd = scrapy.Field() # 主场赔率
    result = scrapy.Field() # 赔率结果
    right_odd = scrapy.Field() #客场赔率
    status = scrapy.Field() # 赔率状态 - closed: 暂未开盘 finished: 已结束 open: 进行中
    type = scrapy.Field() # 赔率类型





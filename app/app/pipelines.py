# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from app.items import EsportNews
import requests
import json
import app.items as Items
from scrapy.utils.project import get_project_settings # 获取项目配置
from app.utils.tools import download_file

class AppPipeline(object):
    def process_item(self, item, spider):
        return item

class QmplanPipeline(object):

    cache_team_competion = {}

    def open_spider(self, spider):
        pass

    # 向后台发送Post请求
    def post(self, api, data = {}, files = {} ):
        settings = get_project_settings()
        qmplan =  dict(settings.get('QMPLAN'))
        host = qmplan['host']
        ver = qmplan['ver']
        url = "%s/%s%s" % (host, ver, api)
        return requests.post(url, data=data, files=files, headers = {
            'X-Token': qmplan['token'],
            'Admin-Token': qmplan['admin_token']
        })

    # 向后台上传文件
    def upload_file(self, filepath):
        files = {
            "file": open(filepath, 'rb'),
        }
        res = self.post("/file/upload", files=files)
        data = res.json()
        if data['code'] == 200:
            return data['data']
        else:
            raise Exception(u"上传文件出错 %s" % data['msg'])

    def process_item(self, item, spider):

        # 电竞资讯采集
        if isinstance(item, EsportNews):
            res = self.post("/pages/save", data ={
                'title': item['title'],
                'body': item['content'],
                'subtitle': item['title'],
                'type': '14',
                'code': item['id'],
            })

        # 电竞战队
        if isinstance(item, Items.EsportTeam):
            
            logo = item['logo']
            filepath = download_file(logo)
            remote_path = self.upload_file(filepath)

            res = self.post("/admin/esports/team/save", data= {
                "name": item['tag'],
                "logo": remote_path,
                "desc": "",
                "extern_id": item["id"],
            })

        # 电竞赛事
        if isinstance(item, Items.EsportComeption):

            self.post("/admin/esports/competion/save", data = {
                "title": item["title"],
                "platform": item["platform"],
            })

        # 电竞战队赛事
        if isinstance(item, Items.EsportCompetionTeam):
            
            # 根据赛事名称 查询出对应的 电竞赛事
            title = item['league_name']
            res = self.post("/admin/esports/competion/info", data = {
                'title': title
            })
            data = res.json()
            if data['code'] != 200:
                raise Exception(data["msg"])

            competion_id = data["data"]['id'] # 赛事ID
            
            # 战队信息
            lteam = item['left_team']
            lteam_extern_id = lteam['id']

            res = self.post('/admin/esports/team/info', data = {
                'externID': lteam_extern_id
            })
            data = res.json()
            if data['code'] != 200:
                raise Exception(data['msg'])
            lteam_id = data['data']['id']

            rteam = item['right_team']
            rteam_extern_id = rteam['id']
            res = self.post('/admin/esports/team/info', data = {
                'externID': rteam_extern_id
            })
            data = res.json()
            if data['code'] != 200:
                raise Exception(data["msg"])

            rteam_id = data['data']['id']

            # 后台对应的状态表
            status_mapping = {
                'not_start_yet': 3,
                'ongoing': 0, 
                'finished': 1,
                'canceled': 2,
            }

            # 查询出对应的ID后 保存战队赛事到后台
            res = self.post('/admin/esports/competion/team/save', data={
                'competion': competion_id,
                'lteam': lteam_id,
                'rteam': rteam_id,
                'status': status_mapping[item['status']],
                'round': item['round'],
                'start_time': item['start_time'],
                'extern_id': item['id'],
            })
            data = res.json()
            if data['code'] != 200:
                raise Exception(data['msg'])

        if isinstance(item, Items.EsportPankou):
            
            # 获取战队赛事ID
            team_competion = 0
            team_competion_extern_id = item['team_competion']
            if team_competion_extern_id in self.cache_team_competion:
                team_competion = self.cache_team_competion[team_competion_extern_id]
            else:
                res = self.post('/admin/esports/competion/team/info', data={
                    'externID': team_competion_extern_id
                })
                data = res.json()
                if data['code'] != 200:
                    raise Exception(data['msg'])
                team_competion = data["data"]["id"]

            res = self.post('/admin/esports/odd/pankou/save', data={
                'cteam': team_competion,
                'gameNo': item['game_no'],
                'type': item['type'],
                'key': item['key'],
                'externID': item['id'],
                'killCount': item['kill_count'],
                'value': item['value'],
                'handicap': item['handicap'],
                'topicableType': item['topicable_type'],
            })

            data = res.json()
            if data['code'] != 200:
                raise Exception(data['msg'])
            
            pankou_id = data['data']['id']
            for odd in item['bet_topics']:
                self.post('/admin/esports/odd/save', data={
                    'pankou': pankou_id,
                    'cteam': team_competion,
                    'lodd': odd['left_odd'],
                    'rodd': odd['right_odd'],
                    'externID': odd['id'],
                    'inPlay': odd['in_play'],
                    'status': odd['status'],
                    'checkoutStatus': odd['checkout_status'],
                    'result': odd['result'],
                    'type': odd['type'],
                })
            
        
        return item

    def close_spider(self, spider):
        pass
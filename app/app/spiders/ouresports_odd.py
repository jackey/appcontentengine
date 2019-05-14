# -*- coding: utf-8 -*-


'''
  buildTopicName: function(a, t, s, e, n) {
      var i = null;
      switch (a.type) {
      case "OverUnderTopic":
          1 === n || a.result ? i = "大于" + a.value : 2 !== n && !1 !== a.result || (i = "小于" + a.value);
          break;
      case "OddEvenTopic":
          1 === n || a.result ? i = "奇数" : 2 !== n && !1 !== a.result || (i = "偶数");
          break;
      case "DurationTopic":
          1 === n || a.result ? i = "大于" + Math.round(a.value / 60) + "分钟" : 2 !== n && !1 !== a.result || (i = "小于" + Math.round(a.value / 60) + "分钟");
          break;
      case "KillStreakTopic":
          1 === n || a.result ? i = "有" : 2 !== n && !1 !== a.result || (i = "没有");
          break;
      case "MapOverUnderTopic":
          1 === n || a.result ? i = "高于" + a.value : 2 !== n && !1 !== a.result || (i = "低于" + a.value);
          break;
      case "OvertimeTopic":
          1 === n || a.result ? i = "有" : 2 !== n && !1 !== a.result || (i = "没有");
      default:
          1 === n || a.result ? i = t : 2 !== n && !1 !== a.result || (i = s)
      }
      switch (i || (i = this.$t("topicName.unknown")),
      a.type) {
      case "WinTopic":
          return (0 === a.game_no ? this.$t("topicName.seriesScore") : this.buildGameNo(a.game_no, e)) + i + "胜";
      case "KillTopic":
          return this.buildGameNo(a.game_no, e) + i + this.formatKillNumber(a.value) + "杀";
      case "FirstBloodTopic":
          return this.buildGameNo(a.game_no, e) + i + "一血";
      case "FirstTowerTopic":
          return this.buildGameNo(a.game_no, e) + i + "首个防御塔";
      case "HandicapTopic":
          return n && 2 === n ? i + (a.value > 0 ? -a.value : "+" + -a.value) : i + (a.value > 0 ? "+" + a.value : a.value);
      case "OverUnderTopic":
          return 2 === a.game_id ? this.buildGameNo(a.game_no, e) + "回合总数大小" + i : this.buildGameNo(a.game_no, e) + "人头" + i;
      case "MapHandicapTopic":
          return n && 2 === n ? this.buildGameNo(a.game_no, e) + i + (a.value > 0 ? -a.value : "+" + -a.value) : this.buildGameNo(a.game_no, e) + i + (a.value > 0 ? "+" + a.value : a.value);
      case "OddEvenTopic":
          return 2 === a.game_id ? this.buildGameNo(a.game_no, e) + "比分" + i : this.buildGameNo(a.game_no, e) + "人头" + i;
      case "DurationTopic":
          return this.buildGameNo(a.game_no, e) + i;
      case "KillStreakTopic":
          return this.buildGameNo(a.game_no, e) + i + (5 === a.value ? "暴走" : 8 === a.value ? "超神" : "");
      case "MapOverUnderTopic":
          return this.buildGameNo(a.game_no, e) + "地图数" + i;
      case "BigBossTopic":
          switch (a.key) {
          case "Roshan":
              return this.buildGameNo(a.game_no, e) + i + "首个肉山";
          case "Baron":
              return this.buildGameNo(a.game_no, e) + i + "首条大龙";
          case "Dragon":
              return this.buildGameNo(a.game_no, e) + i + "首条小龙"
          }
      case "PistolTopic":
          return this.buildGameNo(a.game_no, e) + ("first" === a.key ? "上半场" : "下半场") + "手枪局" + i + "胜";
      case "MapFirstScoreTopic":
          return this.buildGameNo(a.game_no, e) + ("first" === a.key ? "上半场" : "下半场") + this.formatKillNumber(a.value) + "回合" + i + "胜";
      case "OvertimeTopic":
          return this.buildGameNo(a.game_no, e) + i + "加时"
      }
  },
  buildBetTopicName: function(a, t, s, e) {
      var n = void 0;
      switch (a.topic_type) {
      case "OverUnderTopic":
          n = t ? "大于" + a.value : "小于" + a.value;
          break;
      case "OddEvenTopic":
          n = t ? "奇数" : "偶数";
          break;
      case "DurationTopic":
          n = t ? "大于" + Math.round(a.value / 60) + "分钟" : "小于" + Math.round(a.value / 60) + "分钟";
          break;
      case "KillStreakTopic":
          n = t ? "有" : "没有";
          break;
      case "MapOverUnderTopic":
          n = t ? "高于" + a.value : "低于" + a.value;
          break;
      case "OvertimeTopic":
          n = t ? "有" : "没有";
          break;
      default:
          n = t ? a.left : a.right
      }
      switch (n || (n = this.$t("topicName.unknown")),
      a.topic_type) {
      case "WinTopic":
          return (0 === a.game_no ? this.$t("topicName.seriesScore") : this.buildGameNo(a.game_no, s)) + n + "胜";
      case "KillTopic":
          return this.buildGameNo(a.game_no, s) + n + this.formatKillNumber(a.value) + "杀";
      case "FirstBloodTopic":
          return this.buildGameNo(a.game_no, s) + n + "一血";
      case "FirstTowerTopic":
          return this.buildGameNo(a.game_no, s) + n + "首个防御塔";
      case "HandicapTopic":
          return t ? n + (a.value > 0 ? "+" + a.value : a.value) : n + (a.value > 0 ? -a.value : "+" + -a.value);
      case "OverUnderTopic":
          return 2 === a.game_id || 2 === e ? this.buildGameNo(a.game_no, s) + "回合总数大小" + n : this.buildGameNo(a.game_no, s) + "人头" + n;
      case "MapHandicapTopic":
          return t ? this.buildGameNo(a.game_no, s) + n + (a.value > 0 ? "+" + a.value : a.value) : this.buildGameNo(a.game_no, s) + n + (a.value > 0 ? -a.value : "+" + -a.value);
      case "OddEvenTopic":
          return 2 === a.game_id || 2 === e ? this.buildGameNo(a.game_no, s) + "比分" + n : this.buildGameNo(a.game_no, s) + "人头" + n;
      case "DurationTopic":
          return this.buildGameNo(a.game_no, s) + n;
      case "KillStreakTopic":
          return this.buildGameNo(a.game_no, s) + n + (5 === a.value ? "暴走" : 8 === a.value ? "超神" : "");
      case "MapOverUnderTopic":
          return this.buildGameNo(a.game_no, s) + "地图数" + n;
      case "BigBossTopic":
          switch (a.key) {
          case "Roshan":
              return this.buildGameNo(a.game_no, s) + n + "首个肉山";
          case "Baron":
              return this.buildGameNo(a.game_no, s) + n + "首条大龙";
          case "Dragon":
              return this.buildGameNo(a.game_no, s) + n + "首条小龙"
          }
      case "PistolTopic":
          return this.buildGameNo(a.game_no, s) + ("first" === a.key ? "上半场" : "下半场") + "手枪局" + n + "胜";
      case "MapFirstScoreTopic":
          return this.buildGameNo(a.game_no, s) + ("first" === a.key ? "上半场" : "下半场") + this.formatKillNumber(a.value) + "回合" + n + "胜";
      case "OvertimeTopic":
          return this.buildGameNo(a.game_no, s) + n + "加时"
      }
  },
  topicPriText: function(a, t, s) {
      var e = void 0;
      switch (a.topic_type ? a.topic_type : a.type) {
      case "OverUnderTopic":
          e = t ? "大于" + a.value : "小于" + a.value;
          break;
      case "OddEvenTopic":
          e = t ? "奇数" : "偶数";
          break;
      case "DurationTopic":
          e = t ? "大于" + Math.round(a.value / 60) + "分钟" : "小于" + Math.round(a.value / 60) + "分钟";
          break;
      case "KillStreakTopic":
          e = t ? "有" : "没有";
          break;
      case "MapOverUnderTopic":
          e = t ? "高于" + a.value : "低于" + a.value;
          break;
      case "OvertimeTopic":
          e = t ? "有" : "没有";
          break;
      default:
          e = t ? a.left : a.right
      }
      return e || (e = this.$t("topicName.unknown")),
      (a.topic_type ? a.topic_type.indexOf("Handicap") > -1 : a.type.indexOf("Handicap") > -1) && (e += t ? " " + (a.value > 0 ? "+" + a.value : a.value) : " " + (a.value > 0 ? -a.value : "+" + -a.value)),
      e
  },
  buildGameNo: function(a, t, s) {
      if (a = Number(a),
      "zh" !== t)
          return "Game " + a + " ";
      if (2 === s)
          return a ? "地图" + a : "全场";
      switch (a) {
      case 0:
          return "全场";
      case 1:
          return "第一局";
      case 2:
          return "第二局";
      case 3:
          return "第三局";
      case 4:
          return "第四局";
      case 5:
          return "第五局";
      case 6:
          return "第六局";
      case 7:
          return "第七局";
      default:
          return "未知场次"
      }
  },
  formatKillNumber: function(a) {
      switch (a) {
      case 1:
          return "一";
      case 2:
          return "二";
      case 3:
          return "三";
      case 4:
          return "四";
      case 5:
          return "五";
      case 6:
          return "六";
      case 7:
          return "七";
      case 8:
          return "八";
      case 9:
          return "九";
      case 10:
          return "十";
      case 11:
          return "十一";
      case 12:
          return "十二";
      case 13:
          return "十三";
      case 14:
          return "十四";
      case 15:
          return "十五";
      case 16:
          return "十六";
      case 17:
          return "十七";
      case 18:
          return "十八";
      case 19:
          return "十九";
      case 20:
          return "二十";
      default:
          return "十"
      }
  },
  formatTopicTitle: function(a, t, s) {
      switch (a.topic_type ? a.topic_type : a.type) {
      case "WinTopic":
          return "获胜者";
      case "HandicapTopic":
          return "比赛让分";
      case "KillTopic":
          return "率先获得" + this.formatKillNumber(a.value) + "杀";
      case "FirstBloodTopic":
          return "率先获得一血";
      case "OddEvenTopic":
          return 2 === t ? "回合总数奇偶" : "人头总数奇偶";
      case "OverUnderTopic":
          return 2 === t ? "回合总数大小" : "人头总数大小";
      case "DurationTopic":
          return "地图比赛时间大小";
      case "KillStreakTopic":
          return "是否出现" + (5 === a.value ? "暴走" : 8 === a.value ? "超神" : "");
      case "MapOverUnderTopic":
          return "比分总数大小";
      case "BigBossTopic":
          switch (a.key) {
          case "Roshan":
              return "击杀首个肉山";
          case "Baron":
              return "击杀首条大龙";
          case "Dragon":
              return "击杀首条小龙"
          }
      case "FirstTowerTopic":
          return "率先获得一塔";
      case "MapHandicapTopic":
          return "回合让分";
      case "PistolTopic":
          return ("first" === a.key ? "上半场手枪局" : "下半场手枪局") + "获胜者";
      case "MapFirstScoreTopic":
          return "率先赢得" + this.formatKillNumber(a.value) + "个回合者";
      case "OvertimeTopic":
          return "是否有加时"
      }
  },
'''

import scrapy
import json
import app.items as Items
import app.utils.tools as Tools
from datetime import datetime

class OuresportsOdd(scrapy.Spider):
  name = "ouresports_odd"

  per = 99
  start_url = "http://api.ouresports.com/api/bets/series?per=%d" % per

  odd_url = "http://api.ouresports.com/api/bets/series/%s/topics"

  game_mapping = {
    '3': 'lol',
    '2':  'csgo',
    '1': 'dota2',
    '4': 'kog'
  }

  def start_requests(self):
    yield scrapy.Request(self.start_url, callback=self.parse_competion_team )


  def parse_competion_team(self, response):
      body = response.body_as_unicode()
      data = json.loads(body)

      # 检查数据是否全面
      if data['meta']['per'] > data['meta']['total_count']:
          match_series = data['match_series']
        
          # 解析比赛赛事数据
          for match_seria in match_series:

              game_id = match_seria['game_id']
              platform = self.game_mapping[str(game_id)]

              # 主场战队
              lteam = Items.EsportTeam()
              lteam['id'] = match_seria['left_team']['id']
              lteam['logo'] = match_seria['left_team']['logo']
              lteam['tag'] = match_seria['left_team']['tag']
              yield lteam

              # 客场战队
              rteam = Items.EsportTeam()
              rteam['id'] = match_seria['right_team']['id']
              rteam['logo'] = match_seria['right_team']['logo']
              rteam['tag'] = match_seria['right_team']['tag']
              yield rteam

              # 赛事
              competion = Items.EsportComeption()
              competion['title'] = match_seria['league_name']
              competion['platform'] = platform
              yield competion

              # 战队赛事
              team_competion = Items.EsportCompetionTeam()
              team_competion['bet_topic_count'] = match_seria['bet_topic_count']
              team_competion['game_platform'] = platform
              team_competion['id'] = match_seria['id']
              team_competion['in_play'] = match_seria['in_play']
              team_competion['league_name'] = match_seria['league_name']
              team_competion['left_team'] = dict(lteam)
              team_competion['right_team'] = dict(rteam)
              team_competion['round'] = match_seria['round']
              # 解析时间字符串
              team_competion['start_time']  = match_seria['start_time']
              team_competion['status'] = match_seria['status']
              yield team_competion

              yield scrapy.Request(self.odd_url % team_competion['id'], callback=self.parse_odd, meta={
                  "team_competion": team_competion['id']
              })

              #break # 测试用
    
  def parse_odd(self, response):
    data = json.loads(response.body_as_unicode())
    team_competion = response.meta['team_competion']
    
    topics = data['topics']

    for topic in topics:

        # 盘口
        pankou = Items.EsportPankou()
        pankou['id'] = topic['id']
        pankou['game_no'] = topic['game_no']
        pankou['end_time'] = topic['end_time']
        pankou['handicap'] = topic['handicap']
        pankou['key'] = topic['key']
        pankou['kill_count'] = topic['kill_count']
        pankou['type'] = topic['type']
        pankou['topicable_type'] = topic['topicable_type']
        pankou['value'] = topic['value']
        pankou['team_competion'] = team_competion

        # 赔率
        bet_topics = topic['bet_topics']
        odds = []
        for bet_topic in bet_topics:
            odd = Items.EsportPankouOdd()
            odd['id'] = bet_topic['id']
            odd['checkout_status'] = bet_topic['checkout_status']
            odd['in_play'] = bet_topic['in_play']
            odd['left_odd'] = bet_topic['left_odd']
            odd['result'] = bet_topic['result']
            odd['right_odd'] = bet_topic['right_odd']
            odd['status'] = bet_topic['status']
            odd['type'] = bet_topic['type']
            odds.append(dict(odd))

        pankou['bet_topics'] = odds

        yield pankou

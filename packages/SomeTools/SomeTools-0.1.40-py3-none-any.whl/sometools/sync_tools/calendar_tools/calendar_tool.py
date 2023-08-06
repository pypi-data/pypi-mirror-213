import requests
import datetime

from lxml import etree
from sometools.sync_tools.base import Base

global calendar_hashmap
calendar_hashmap = dict()


class CalendarMixIn(Base):

    def __init__(self, *args, **kwargs):
        super(CalendarMixIn, self).__init__(*args, **kwargs)

    @staticmethod
    def get_calendar_hashmap() -> dict:
        global calendar_hashmap
        now_datetime = datetime.datetime.now()
        url = f"https://wannianrili.bmcx.com/"
        headers = {
            "Host": "wannianrili.bmcx.com",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0",
            "Accept": "text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01",
            "Accept-Language": "en-US,zh-CN;q=0.8,zh;q=0.7,zh-TW;q=0.5,zh-HK;q=0.3,en;q=0.2",
            "Accept-Encoding": "gzip, deflate, br",
            "X-Requested-With": "XMLHttpRequest",
            "Connection": "keep-alive",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache"
        }
        if calendar_hashmap and calendar_hashmap.get('all_date'):
            print("calendar_hashmap已存在")
            if now_datetime.strftime("%Y-%m-%d") not in calendar_hashmap.get('all_date'):
                print("清空calendar_hashmap")
                calendar_hashmap = dict()
        if not calendar_hashmap:
            print("calendar_hashmap为空")
            res = requests.get(url, headers=headers, timeout=30)
            html_tree = etree.HTML(res.text)
            calendar_hashmap['all_date'] = [i.replace("/", '').replace("__wannianrili", '') for i in
                                            html_tree.xpath("//div[@class='wnrl_riqi']/a/@href")]
            calendar_hashmap['holiday'] = [i.replace("/", '').replace("__wannianrili", '') for i in
                                           html_tree.xpath("//a[@class='wnrl_riqi_xiu']/@href")]  # 休
            calendar_hashmap[90] = [i.replace("/", '').replace("__wannianrili", '') for i in
                                    html_tree.xpath("//a[@class='wnrl_riqi_ban']/@href")]  # 调休工作日
            calendar_hashmap['weekend'] = [i.replace("/", '').replace("__wannianrili", '') for i in
                                           html_tree.xpath("//a[@class='wnrl_riqi_mo']/@href")]  # 周末
            calendar_hashmap[0] = set(calendar_hashmap['all_date']) - set(calendar_hashmap['holiday']) - set(
                calendar_hashmap['weekend']) - set(calendar_hashmap[90])  # 正常工作日
        return calendar_hashmap
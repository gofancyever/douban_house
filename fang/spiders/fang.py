import re
import scrapy
from bs4 import BeautifulSoup
from scrapy.http import Request
from fang.items import FangItem
from configparser import ConfigParser
import ast
from datetime import datetime



cf = ConfigParser()
cf.read("config.ini")

location_list = ast.literal_eval(cf.get("DEFAULT", "location"))
starttime_str = cf.get('DEFAULT','start_time')


# https://m.douban.com/group/beijingzufang/?start=0
class HouseSpider(scrapy.Spider):
    name = 'fang'
    allowed_domains = ['douban.com']
    baseUrl = "https://m.douban.com/group"
    group = 'beijingzufang'
    handle_httpstatus_list = [302]
    cyclic = True
    def start_requests(self):
        i = 0
        while self.cyclic:
            url = 'https://m.douban.com/group/beijingzufang/?start={}'.format(str(i*25))
            yield Request(url,self.parse)
            i+=1

        # for i in range(0,2):
        #     url = '{}/{}/discussion?start={}'.format(self.baseUrl,self.group,str(i*50))
        #     yield Request(url,self.parse)
    def parse(self, response):
        soup = BeautifulSoup(response.text,'lxml')
        ul = soup.find('ul',class_='base-list')
        li = ul.find_all('li')
        items = []
        for a in li:
            a_last = a.find_all('a')[-1]
            title = a_last.get('title').replace('\xa0','')
            href = a_last.get('href')
            href = 'https://m.douban.com{}'.format(href)
            time = a_last.find('span',class_='right').string.replace('\xa0','')
            time = ''.join(time.split())

            # 过滤不符合条件
            date = datetime.strptime(time, '%m-%d%H:%S')
            start_time = datetime.strptime(starttime_str,'%m-%d')
            if not date > start_time:
                self.cyclic = False
                print('不符合时间')
                break

            if not self.filterData(title,location_list):
                print('不符合条件')
                continue

            print('ok,{}'.format(title))
            item = FangItem()
            item['title'] = title
            item['time'] = time
            item['url'] = href
            items.append(item)
        return items

    def filterData(self,data,location_list):
        res = False
        for loc in location_list:
            if data.find(loc) > 0:
                res = True
                continue
        return res
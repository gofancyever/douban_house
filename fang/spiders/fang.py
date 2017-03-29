import re
import scrapy
from bs4 import BeautifulSoup
from scrapy.http import Request
from fang.items import FangItem



# https://m.douban.com/group/beijingzufang/?start=0
class HouseSpider(scrapy.Spider):
    name = 'fang'
    allowed_domains = ['douban.com']
    baseUrl = "https://m.douban.com/group"
    group = 'beijingzufang'
    handle_httpstatus_list = [302]

    def start_requests(self):
        url = 'https://m.douban.com/group/beijingzufang/?start=0'
        yield Request(url,self.parse)
        # for i in range(0,2):
        #     url = '{}/{}/discussion?start={}'.format(self.baseUrl,self.group,str(i*50))
        #     yield Request(url,self.parse)
    def parse(self, response):
        print(response.text)
        print()
        soup = BeautifulSoup(response.text,'lxml')
        ul = soup.find('ul',class_='base-list')
        li = ul.find_all('li')
        for a in li:
            a_last = a.find_all('a')[-1]
            title = a_last.get('title')
            href = a_last.get('href')
            time = a_last.find('span',class_='right').string
            print('ok')
            item = FangItem()
            item.title = str(title.replace('\xa0',''))
            item.time = str(time.replace('\xa0',''))
            item.url = 'https://m.douban.com{}'.format(href)
            return item

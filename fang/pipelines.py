# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from fang.items import FangItem
from fang.sql import Sql

class FangPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item,FangItem,spider):
            url = item['url']
            ret = Sql.select_url(url)
            if len(ret)>0:
                print('已经存在')
                pass
            else:
                title = item['title']
                time = item['time']
                loc = item['loc']
                url = item['url']
                Sql.insert_item(title,loc,time,url)

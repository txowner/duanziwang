# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
import re
import time

class SaveMongoPipeline(object):
    """
    1、pipeline 用来处理item传递过来的数据
    2、将数据进行特定处理后，存入mongodb
    """
    def __init__(self, mongo_uri, mongo_db, mongo_user, mongo_passwd):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.mongo_user = mongo_user
        self.mongo_passwd = mongo_passwd

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get("MONGO_URI"),
            mongo_db=crawler.settings.get("MONGO_DB"),
            mongo_user=crawler.settings.get("MONGO_USER"),
            mongo_passwd=crawler.settings.get("MONGO_PASSWD"),
        )

    def parse_time(self, pub_date):
        """
        xx天前( 4天前)、 xx周前(2周前 (11-21))、 xx月前(12个月前 (12-10))、 xx年前(1年前 (2016-11-30))
        :param pub_date: 
        :return: 
        """
        if pub_date:
            if re.match('(\d+)天前', pub_date):
                day = re.match('(\d+)天前', pub_date).group(1)
                pub_date = time.strftime("%Y-%m-%d", time.localtime(time.time() - float(day)*24*60*60))
            if re.match('.*?周前.*?\((.*?)\)', pub_date):
                date = re.match('.*?周前.*?\((.*?)\)', pub_date).group(1)
                pub_date = time.strftime("%Y"+"-%s"%date, time.localtime())
            if re.match('.*个月前.*?\((.*?)\)', pub_date):
                date = re.match('.*个月前.*?\((.*?)\)', pub_date).group(1)
                month, day = date.split('-')
                t = time.localtime()
                y = t.tm_year
                m = t.tm_mon
                if m - month >0:
                    pub_date = "%s-%s-%s" %(y,month, day)
                else:
                    pub_date = "%s-%s-%s" % (y-1, month, day)
            if re.match(".*?年前.*?\((.*?)\)", pub_date):
                pub_date = re.match(".*?年前.*?\((.*?)\)", pub_date).group(1)

            return pub_date

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.client['admin'].authenticate(self.mongo_user, self.mongo_passwd)
        self.db = self.client[self.mongo_db]

    def process_item(self, item, spider):
        """
        先处理日期问题， 再存入mongodb， 注意，一定要返回item or Dropitem
        :param item: 
        :param spider: 
        :return: 
        """
        item['publish_date'] = self.parse_time(item['publish_date'])
        collection_name = item.__class__.__name__
        self.db[collection_name].update({'url': item['url']}, {'$set': item}, True)
        return item

    def close_spider(self, spider):
        self.client.close()
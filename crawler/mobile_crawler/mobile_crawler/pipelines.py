# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
import traceback

class ConsolePipeline(object):

    def process_item(self, item, spider):
        print item
        return item

class MongoDBPipeline(object):

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(host='192.168.0.21', port=27017)
        self.db = self.client['test']
        self.db.authenticate('root', '123456')

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        try:
            self.db['mobile'].insert(dict(item))
        except pymongo.errors.DuplicateKeyError:
            pass
        except Exception, e:
            print e.message
            print traceback.format_exc()
        return item
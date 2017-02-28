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
        self.client = pymongo.MongoClient(host='192.168.0.20', port=27018)
        self.db = self.client['mobile']
        # self.db.authenticate('root', '123456')

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        try:
            dbitem = self.db['mobile'].find_one({'mobile': item['mobile'], 'name': ''})
            if dbitem:
                if item['name'] and item['name'] != '':
                    self.db['mobile'].update_one({'mobile': item['mobile']}, {'$set': {'name': item['name']}})
            else:
                self.db['mobile'].insert(dict(item))
        except pymongo.errors.DuplicateKeyError:
            pass
        except Exception, e:
            print e.message
            print traceback.format_exc()
        return item
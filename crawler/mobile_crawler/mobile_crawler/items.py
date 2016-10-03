# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class MobileItem(scrapy.Item):
    _id = scrapy.Field()
    name = scrapy.Field()
    mobile = scrapy.Field()
    timestamp = scrapy.Field()
    jsonstr = scrapy.Field()
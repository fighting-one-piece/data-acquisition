# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class QQGroupItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    _id = scrapy.Field()
    groupCode = scrapy.Field()
    groupFlag = scrapy.Field()
    groupLevel = scrapy.Field()
    groupMemNum = scrapy.Field()
    groupMaxMem = scrapy.Field()
    groupOwner = scrapy.Field()
    groupName = scrapy.Field()
    groupIntro = scrapy.Field()
    groupTags = scrapy.Field()
    groupClass = scrapy.Field()
    groupClass2 = scrapy.Field()
    groupClassText = scrapy.Field()
    pass

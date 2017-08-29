# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WeiboItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
	uid = scrapy.Field()
	cid = scrapy.Field()
	name = scrapy.Field()
	time = scrapy.Field()
	text = scrapy.Field()
	source = scrapy.Field()
	sex = scrapy.Field()
	location = scrapy.Field()
	intro = scrapy.Field()
	# level = scrapy.Field()
	regi_date = scrapy.Field()
	# credit = scrapy.Field()



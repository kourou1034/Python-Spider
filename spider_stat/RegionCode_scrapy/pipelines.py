# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from openpyxl import Workbook

class RegioncodePipeline(object):
	wb = Workbook()
	ws = wb.active
	ws.append(['code', 'name'])

	def process_item(self, item, spider):
		line = [item['code'], item['name']]
		self.ws.append(line)
		self.wb.save('C:\\Users\\Think\\desktop\\code1.xlsx')
		return item

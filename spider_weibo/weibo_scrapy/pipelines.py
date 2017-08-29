# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql.cursors
import pymysql
from openpyxl import Workbook

class WeiboPipeline(object):
	wb = Workbook()
	ws = wb.active
	ws.append(['cid', 'uid', 'name',  'time', 'text', 'source', 'sex', 'location', 'intro', 'regi_date'])
	
	def process_item(self, item, spider):
		line = [item['cid'],item['uid'],item['name'],item['time'],item['text'],item['source'],item['sex'],item['location'],item['intro'],item['regi_date']]
		self.ws.append(line)
		self.wb.save('C:\\Users\\Think\\desktop\\weibo\\weibo624-3.xlsx')
		return item
		# conn = pymysql.connect(host='localhost',
		# 	port=3306,
		# 	user='root',
		# 	password='12345678',
		# 	db='weibo',
		# 	charset='utf8mb4')
		# cur = conn.cursor()

		# cur.execute("create table if not exists comment(uid char(100), name char(100), time char(100), "
		# 	"text text(255), source char(100), sex char(10), location char(100), intro text(100),"
		# 	"level char(20), regi_date char(40), credit char(20)) DEFAULT CHARSET=utf8mb4")
		# sql = ("insert into comment(uid,name,time,text,source,sex,location,intro,level,regi_date,credit) value(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
		# lis = (item['uid'],item['name'],item['time'],item['text'],item['source'],item['sex'],item['location'],item['intro'],item['level'],item['regi_date'],item['credit'])
		# try:
		# 	cur.execute(sql, lis)
		# except Exception as e:
		# 	print("Insert error:", e)
		# 	conn.rollback()
		# else:
		# 	conn.commit()
		# cur.close()
		# conn.close()
		# return item

# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql.cursors
import pymysql

class Music163Pipeline(object):
    def process_item(self, item, spider):
        conn = pymysql.connect(host='localhost',
        	port=3306,
        	user='root',
        	password='12345678',
        	db='music163',
        	charset='UTF8')
        cur = conn.cursors()
        cur.execute("create table if not exists music(artist CHAR(40), song CHAR(40), comment CHAR(20), url CHAR(40))")
        sql = ("insert into music(artist, song, comment, url) value(%s, %s, %s, %s")
        lis = (item['artist'], item['song'], item['comment'], item['url'])
        try:
        	cur.execute(sql, lis)
        except Exception as e:
        	print("Insert error:", e)
        	conn.rollback()
        else:
        	conn.commit()
        cur.close()
        conn.close()

        return item

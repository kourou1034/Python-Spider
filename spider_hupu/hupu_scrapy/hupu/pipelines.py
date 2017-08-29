# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql.cursors
import pymysql

class HupuPipeline(object):
    def process_item(self, item, spider):
        
        conn = pymysql.connect(host='localhost',
                       port=3306,
                       user='root',
                       password='12345678',
                       db='hupu_bxj',
                       charset='UTF8') 
        cur = conn.cursor()
        cur.execute("create table if not exists bxj(title CHAR(255), author CHAR(20), time CHAR(20), artical char(200), url char(100))")
        sql = ("insert into bxj(title,author,time,artical,url) "
               "value(%s,%s,%s,%s,%s)")
        lis = (item['title'],item['author'],item['time'],item['artical'],item['url'])
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

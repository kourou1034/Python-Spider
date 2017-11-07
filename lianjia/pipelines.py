# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql.cursors
import pymysql

class LianjiaPipeline(object):
    def process_item(self, item, spider):
        conn = pymysql.connect(host='localhost',
        	port=3306,
        	user='root',
        	password='12345678',
        	db='lianjia_beijing_zaishou',
        	charset='UTF8')
        cur = conn.cursor()

        #已成交
        # sql1 = '''CREATE TABLE IF NOT EXISTS ershoufang_yanjiao(href VARCHAR(100),
        # qu VARCHAR(100), jiedao VARCHAR(100), name VARCHAR(100), jishijiting 
        # VARCHAR(100), totalPrice VARCHAR(100),initPrice VARCHAR(100),unitPrice
        #  VARCHAR(100),dealTime VARCHAR(100),jiaoyipingtai VARCHAR(100),
        #   houseFloor VARCHAR(100), houseArea VARCHAR(100), houseStructure VARCHAR(100), 
        #   huxingjiegou VARCHAR(100),actualArea VARCHAR(100),buildingType 
        # VARCHAR(100),houseOrientation VARCHAR(100), houseDate VARCHAR(100),
        # Decoration VARCHAR(100), jianzhujiegou VARCHAR(100), gongnuanfangshi 
        # VARCHAR(100), ladder VARCHAR(100),tihubili VARCHAR(100), chanquannianxian
        #  VARCHAR(100), fangwunianxian VARCHAR(100),fangwuyongtu VARCHAR(100),
        #  fangyuanbiaoqian VARCHAR(100),hexinmaidian VARCHAR(1024),shuifeijiexi VARCHAR(1024),
        #  jiaotongchuxing VARCHAR(1024),zhoubianpeitao VARCHAR(1024),huxingjieshao VARCHAR(1024),
        #  xiaoqujieshao VARCHAR(1024),quanshudiya VARCHAR(1024),shoufangxiangqing VARCHAR(1024),
        #  fangzhuzijian VARCHAR(1024))
        # '''


        #在售
        sql1 = '''CREATE TABLE IF NOT EXISTS ershoufang_xianghe(href VARCHAR(100),
        qu VARCHAR(100), jiedao VARCHAR(100), name VARCHAR(100),xiaoqumingchen VARCHAR(1024), 
        totalPrice VARCHAR(100),unitPrice VARCHAR(100),fangwuhuxing VARCHAR(100),
          houseFloor VARCHAR(100), houseArea VARCHAR(100), houseStructure VARCHAR(100), 
          huxingjiegou VARCHAR(100),actualArea VARCHAR(100),buildingType 
        VARCHAR(100),houseOrientation VARCHAR(100), houseDate VARCHAR(100),
        Decoration VARCHAR(100), jianzhujiegou VARCHAR(100), gongnuanfangshi 
        VARCHAR(100), ladder VARCHAR(100),tihubili VARCHAR(100), chanquannianxian
         VARCHAR(100), fangwunianxian VARCHAR(100),fangwuyongtu VARCHAR(100),
         fangyuanbiaoqian VARCHAR(100),hexinmaidian VARCHAR(1024),shuifeijiexi VARCHAR(1024),
         jiaotongchuxing VARCHAR(1024),zhoubianpeitao VARCHAR(1024),huxingjieshao VARCHAR(1024),
         xiaoqujieshao VARCHAR(1024),quanshudiya VARCHAR(1024),shoufangxiangqing VARCHAR(1024),
         fangzhuzijian VARCHAR(1024),jiaoyiquanshu VARCHAR(1024),
         guapaishijian VARCHAR(1024), shangcijiaoyi VARCHAR(1024),chanquansuoshu VARCHAR(1024),
         fangbentiaojian VARCHAR(1024),diyaxinxi VARCHAR(1024))
        '''

        cur.execute(sql1)

        #已成交
        # sql2 = '''INSERT INTO ershoufang_yanjiao(href,qu,jiedao,name,jishijiting,totalPrice,
        # initPrice,unitPrice,dealTime,jiaoyipingtai,houseFloor,houseArea,houseStructure,
        # huxingjiegou,actualArea,buildingType,houseOrientation,houseDate,Decoration,jianzhujiegou,
        # gongnuanfangshi,ladder,tihubili,chanquannianxian,fangwunianxian,fangwuyongtu,
        # fangyuanbiaoqian,hexinmaidian,shuifeijiexi,jiaotongchuxing,zhoubianpeitao,huxingjieshao,
        # xiaoqujieshao,quanshudiya,shoufangxiangqing,fangzhuzijian) value
        # (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
        # lis = (item['href'],item['qu'],item['jiedao'],item['name'],item['jishijiting'],
        # 	item['totalPrice'],item['initPrice'],item['unitPrice'],item['dealTime'],
        # 	item['jiaoyipingtai'],item['houseFloor'],item['houseArea'],item['jianzhumianji'],
        # 	item['huxingjiegou'],item['taoneimianji'],item['buildingType'],item['houseOrientation'],
        # 	item['houseDate'],item['Decoration'],item['jianzhujiegou'],item['gongnuanfangshi'],
        # 	item['ladder'],item['tihubili'],item['chanquannianxian'],item['fangwunianxian'],
        # 	item['fangwuyongtu'],item['fangyuanbiaoqian'],item['hexinmaidian'],item['shuifeijiexi'],
        # 	item['jiaotongchuxing'],item['zhoubianpeitao'],item['huxingjieshao'],item['xiaoqujieshao'],
        # 	item['quanshudiya'],item['shoufangxiangqing'],item['fangzhuzijian']
        # 	)


        #在售
        sql2 = '''INSERT INTO ershoufang_xianghe(href,qu,jiedao,name,xiaoqumingchen,
        totalPrice,unitPrice,fangwuhuxing,houseFloor,houseArea,houseStructure,
        huxingjiegou,actualArea,buildingType,houseOrientation,houseDate,Decoration,jianzhujiegou,
        gongnuanfangshi,ladder,tihubili,chanquannianxian,fangwunianxian,fangwuyongtu,
        fangyuanbiaoqian,hexinmaidian,shuifeijiexi,jiaotongchuxing,zhoubianpeitao,huxingjieshao,
        xiaoqujieshao,quanshudiya,shoufangxiangqing,fangzhuzijian,jiaoyiquanshu,
        guapaishijian,shangcijiaoyi,chanquansuoshu,fangbentiaojian,diyaxinxi) value
        (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
        lis = (item['href'],item['qu'],item['jiedao'],item['name'],item['xiaoqumingchen'],
            item['totalPrice'],item['unitPrice'],item['fangwuhuxing'],
            item['houseFloor'],item['houseArea'],item['jianzhumianji'],
            item['huxingjiegou'],item['taoneimianji'],item['buildingType'],item['houseOrientation'],
            item['houseDate'],item['Decoration'],item['jianzhujiegou'],item['gongnuanfangshi'],
            item['ladder'],item['tihubili'],item['chanquannianxian'],item['fangwunianxian'],
            item['fangwuyongtu'],item['fangyuanbiaoqian'],item['hexinmaidian'],item['shuifeijiexi'],
            item['jiaotongchuxing'],item['zhoubianpeitao'],item['huxingjieshao'],item['xiaoqujieshao'],
            item['quanshudiya'],item['shoufangxiangqing'],item['fangzhuzijian'],item['jiaoyiquanshu'],
            item['guapaishijian'],item['shangcijiaoyi'],item['chanquansuoshu'],item['fangbentiaojian'],
            item['diyaxinxi']
            )

        cur.execute(sql2, lis)
        conn.commit()

        cur.close()
        conn.close()

        return item
# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LianjiaItem(scrapy.Item):

	# 在售字段
	href = scrapy.Field() 				#房源链接
	qu = scrapy.Field() 				#区名
	jiedao = scrapy.Field()				#街道名
	name = scrapy.Field()				#标题
	totalPrice = scrapy.Field()			#成交价
	unitPrice = scrapy.Field()			#单价
	houseFloor = scrapy.Field()			#楼层
	houseArea = scrapy.Field()			#面积
	jianzhumianji = scrapy.Field() 		#建筑面积
	huxingjiegou = scrapy.Field()		#户型结构
	taoneimianji = scrapy.Field()		#套内面积
	buildingType = scrapy.Field()		#建筑类型
	houseOrientation = scrapy.Field()	#房屋朝向
	houseDate = scrapy.Field()			#建成年代
	Decoration = scrapy.Field()			#装修情况
	jianzhujiegou = scrapy.Field()		#建筑结构
	gongnuanfangshi = scrapy.Field()	#供暖方式
	ladder = scrapy.Field()				#是否配有电梯
	tihubili = scrapy.Field()			#梯户比例
	chanquannianxian = scrapy.Field()	#产权年限
	fangwunianxian = scrapy.Field()		#房屋用途年限
	fangwuyongtu = scrapy.Field()		#房屋用途
	fangyuanbiaoqian = scrapy.Field()	#房源标签
	hexinmaidian = scrapy.Field()		#核心卖点
	shuifeijiexi = scrapy.Field()		#税费解析
	jiaotongchuxing = scrapy.Field()	#交通出行
	zhoubianpeitao = scrapy.Field()		#周边配套
	huxingjieshao = scrapy.Field()		#户型介绍
	xiaoqujieshao = scrapy.Field()		#小区介绍
	quanshudiya = scrapy.Field()		#权属抵押
	shoufangxiangqing = scrapy.Field()	#售房详情
	fangzhuzijian = scrapy.Field()		#房主自荐
	xiaoqumingchen = scrapy.Field()		#小区名
	jiaoyiquanshu = scrapy.Field()
	guapaishijian = scrapy.Field()
	shangcijiaoyi = scrapy.Field()
	chanquansuoshu = scrapy.Field()
	fangbentiaojian = scrapy.Field()
	diyaxinxi = scrapy.Field()
	fangwuhuxing = scrapy.Field()


	# 已成交字段
	# href = scrapy.Field() 				#房源链接
	# qu = scrapy.Field() 				#区名
	# jiedao = scrapy.Field()				#街道名
	# name = scrapy.Field()				#标题
	# jishijiting = scrapy.Field()		#几室几厅
	# totalPrice = scrapy.Field()			#成交价
	# initPrice = scrapy.Field()			#挂牌价
	# unitPrice = scrapy.Field()			#单价
	# dealTime = scrapy.Field()			#交易时间
	# jiaoyipingtai = scrapy.Field()		#交易平台	
	# houseFloor = scrapy.Field()			#楼层
	# houseArea = scrapy.Field()			#面积
	# jianzhumianji = scrapy.Field() 		#建筑面积
	# huxingjiegou = scrapy.Field()		#户型结构
	# taoneimianji = scrapy.Field()		#套内面积
	# buildingType = scrapy.Field()		#建筑类型
	# houseOrientation = scrapy.Field()	#房屋朝向
	# houseDate = scrapy.Field()			#建成年代
	# Decoration = scrapy.Field()			#装修情况
	# jianzhujiegou = scrapy.Field()		#建筑结构
	# gongnuanfangshi = scrapy.Field()	#供暖方式
	# ladder = scrapy.Field()				#是否配有电梯
	# tihubili = scrapy.Field()			#梯户比例
	# chanquannianxian = scrapy.Field()	#产权年限
	# fangwunianxian = scrapy.Field()		#房屋用途年限
	# fangwuyongtu = scrapy.Field()		#房屋用途
	# fangyuanbiaoqian = scrapy.Field()	#房源标签
	# hexinmaidian = scrapy.Field()		#核心卖点
	# shuifeijiexi = scrapy.Field()		#税费解析
	# jiaotongchuxing = scrapy.Field()	#交通出行
	# zhoubianpeitao = scrapy.Field()		#周边配套
	# huxingjieshao = scrapy.Field()		#户型介绍
	# xiaoqujieshao = scrapy.Field()		#小区介绍
	# quanshudiya = scrapy.Field()		#权属抵押
	# shoufangxiangqing = scrapy.Field()	#售房详情
	# fangzhuzijian = scrapy.Field()		#房主自荐
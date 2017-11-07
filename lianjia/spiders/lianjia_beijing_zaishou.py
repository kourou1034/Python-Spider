import scrapy
from lianjia.items import LianjiaItem
from bs4 import BeautifulSoup
import time
import requests

class HouseSpider(scrapy.Spider):
	name = 'lianjia_zaishou_beijing'
	allowed_domains = ['bj.lianjia.com/']
	start_urls = ['https://lf.lianjia.com/ershoufang/xianghe/']
	'''
	东城：https://bj.lianjia.com/ershoufang/dongcheng/
	西城：https://bj.lianjia.com/ershoufang/xicheng/
	朝阳：https://bj.lianjia.com/ershoufang/chaoyang/
	海淀：https://bj.lianjia.com/ershoufang/haidian/
	丰台：https://bj.lianjia.com/ershoufang/fengtai/
	石景山：https://bj.lianjia.com/ershoufang/shijingshan/
	通州：https://bj.lianjia.com/ershoufang/tongzhou/
	昌平：https://bj.lianjia.com/ershoufang/changping/
	大兴：https://bj.lianjia.com/ershoufang/daxing/
	亦庄开发区：https://bj.lianjia.com/ershoufang/yizhuangkaifaqu/
	顺义：https://bj.lianjia.com/ershoufang/shunyi/
	房山：https://bj.lianjia.com/ershoufang/fangshan/
	门头沟：https://bj.lianjia.com/ershoufang/mentougou/
	平谷：https://bj.lianjia.com/ershoufang/pinggu/
	怀柔：https://bj.lianjia.com/ershoufang/huairou/
	密云：https://bj.lianjia.com/ershoufang/miyun/
	延庆：https://bj.lianjia.com/ershoufang/yanqing/

	燕郊：https://lf.lianjia.com/ershoufang/yanjiao/
	香河：https://lf.lianjia.com/ershoufang/xianghe/
	'''

	def parse(self, response):
		url = response.url
		for i in range(1,10):
			house_url = url + 'pg' + str(i) + '/'
			yield scrapy.Request(url = house_url,callback=self.get_house_url,dont_filter=True)




	# def parse(self,response):
	# 	data = response.body
	# 	soup = BeautifulSoup(data,'lxml')
	# 	area_href = response.url
	# 	if area_href == 'https://bj.lianjia.com/ershoufang/chaoyang/':
	# 		for i in range(1,6):
	# 			try:
	# 				for n in range(1,90):
	# 					try:
	# 						page_url = area_href+'pg'+str(n)+'lc'+str(i)+'/'
	# 						yield scrapy.Request(page_url, callback=self.get_house_url, dont_filter=True)
	# 					except:
	# 						break
	# 			except:
	# 				pass
	# 	if area_href in ['https://bj.lianjia.com/ershoufang/dongcheng/','https://bj.lianjia.com/ershoufang/xicheng/','https://bj.lianjia.com/ershoufang/tongzhou/','https://bj.lianjia.com/ershoufang/daxing/']:
	# 		for i in range(1,6):
	# 			try:
	# 				for n in range(1,18):
	# 					try:
	# 						page_url = area_href+'pg'+str(n)+'lc'+str(i)+'/'
	# 						yield scrapy.Request(page_url, callback=self.get_house_url, dont_filter=True)
	# 					except:
	# 						break
	# 			except:
	# 				pass

	# 	if area_href in ['https://bj.lianjia.com/ershoufang/fengtai/','https://bj.lianjia.com/ershoufang/fangshan/','https://bj.lianjia.com/ershoufang/shunyi/']:
	# 		for i in range(1,6):
	# 			try:
	# 				for n in range(1,33):
	# 					try:
	# 						page_url = area_href+'pg'+str(n)+'lc'+str(i)+'/'
	# 						yield scrapy.Request(page_url, callback=self.get_house_url, dont_filter=True)
	# 					except:
	# 						break
	# 			except:
	# 				pass

	# 	if area_href in ['https://bj.lianjia.com/ershoufang/yizhuangkaifaqu/','https://bj.lianjia.com/ershoufang/mentougou/','https://bj.lianjia.com/ershoufang/xicheng/']:
	# 		for i in range(1,6):
	# 			try:
	# 				for n in range(1,46):
	# 					try:
	# 						page_url = area_href+'pg'+str(n)+'lc'+str(i)+'/'
	# 						yield scrapy.Request(page_url, callback=self.get_house_url, dont_filter=True)
	# 					except:
	# 						break
	# 			except:
	# 				pass

	# 	if area_href in ['https://bj.lianjia.com/ershoufang/pinggu/','https://bj.lianjia.com/ershoufang/huairou/','https://bj.lianjia.com/ershoufang/miyun/','https://bj.lianjia.com/ershoufang/yanqing/']:
	# 		page_url = area_href+'pg1'+'/'
	# 		yield scrapy.Request(page_url, callback=self.get_house_url, dont_filter=True)


	def get_house_url(self, response):
		print(response.url)
		# 获取每个房源的url，跳转到详细信息页面
		data = response.body
		soup = BeautifulSoup(data, 'lxml')
		ul_ershoufang_house = soup.find('ul',attrs={'class':'sellListContent'})
		div_lists = ul_ershoufang_house.find_all('div', attrs={'class':'title'})
		for div in div_lists:
			label_a = div.find('a')
			house_url = label_a['href']
			yield scrapy.Request(house_url,callback=self.get_house_info,dont_filter=True)

	def get_house_info(self,response):
			print(response.url)
			data = response.body
			soup = BeautifulSoup(data,'lxml')
			item = LianjiaItem()
			item['href'] = response.url
			item['qu'] = soup.find('div', attrs={'class':'fl l-txt'}).find_all('a')[2].getText()[:-3]
			item['jiedao'] = soup.find('div', attrs={'class':'fl l-txt'}).find_all('a')[3].getText()[:-3]
			title = soup.find('div',attrs={'class':'title-wrapper'}	).find('h1').getText()
			item['name'] = title
			item['xiaoqumingchen'] = soup.find('div', attrs={'class':'fl l-txt'}).find_all('a')[4].getText()[:-3]
			try:
				item['totalPrice'] = soup.find('div', attrs={'class':'price'}).find('span').getText()
			except:
				item['totalPrice'] = 0
			try:
				item['unitPrice'] = soup.find('div', attrs={'class':'price'}).find('span',attrs={'class':'unitPriceValue'}).getText()
			except:
				item['unitPrice'] = 0
			base_lists = soup.find('div', attrs={'class':'base'}).find('div', attrs={'class':'content'}).find_all('li')
			item_dict = {'fangwuhuxing':'房屋户型','houseFloor':'所在楼层','jianzhumianji':'建筑面积',
			'huxingjiegou':'户型结构','taoneimianji':'套内面积',
			'buildingType':'建筑类型','houseOrientation':'房屋朝向','houseDate':'建成年代',
			'Decoration':'装修情况','jianzhujiegou':'建筑结构',
			'gongnuanfangshi':'供暖方式','tihubili':'梯户比例','chanquannianxian':'产权年限',
			'ladder':'配备电梯'}
			base_dict = {}
			for li in base_lists:
				label = li.find('span').getText().strip()
				content = li.getText().strip(label)
				base_dict[label] = content
			for i in item_dict.keys():
				if item_dict[i] in base_dict.keys():
					item[i] = base_dict[item_dict[i]]
				else:
					item[i] = ''
			item['houseArea'] = item['jianzhumianji']
			jiaoyi_lists = soup.find('div', attrs={'class':'transaction'}).find_all('li')
			item['fangwuyongtu'] = jiaoyi_lists[3].getText().strip('房屋用途').strip()
			item['fangwunianxian'] = jiaoyi_lists[4].getText().strip('房屋年限').strip()
			item['jiaoyiquanshu'] = jiaoyi_lists[1].getText().strip('交易权属').strip()
			item['diyaxinxi']  = jiaoyi_lists[6].getText().strip('抵押信息').strip()
			item['guapaishijian'] = jiaoyi_lists[0].getText().strip('挂牌时间').strip()
			item['shangcijiaoyi'] = jiaoyi_lists[2].getText().strip('上次交易').strip()
			item['chanquansuoshu'] = jiaoyi_lists[5].getText().strip('产权所属').strip()
			item['fangbentiaojian'] = jiaoyi_lists[7].getText().strip('房本条件').strip()
			#fangyuantese_list = ['fangyuanbiaoqian','hexinmaidian','shuifeijiexi','jiaotongchuxing',
			#'zhoubianpeitao','huxingjieshao','xiaoqujieshao','quanshudiya','shoufangxiangqing']
			#fyts_list_cn = ['核心卖点','税费解析','交通出行','周边配套','户型介绍','小区介绍','权属抵押',
			#'售房详情']
			fyts_name_dict = {'核心卖点':'hexinmaidian','税费解析':'shuifeijiexi','交通出行':'jiaotongchuxing',
			'周边配套':'zhoubianpeitao','户型介绍':'huxingjieshao','小区介绍':'xiaoqujieshao',
			'权属抵押':'quanshudiya','售房详情':'shoufangxiangqing'}
			try:	
				fangyuantese = soup.find('div',attrs={'class':'introContent showbasemore'})
				fangyuanbiaoqian_list = fangyuantese.find('div', attrs={'class':'tags clear'}).find('div',attrs={'class':'content'}).find_all('a')
				fangyuanbiaoqian_txt = ''
				for f in fangyuanbiaoqian_list:
					f_txt = f.getText()
					fangyuanbiaoqian_txt = fangyuanbiaoqian_txt + f_txt + ','
				item['fangyuanbiaoqian'] = fangyuanbiaoqian_txt[:-1]
				fyts_divs = fangyuantese.find_all('div',attrs={'class':'baseattribute clear'})
				fyts_dict = {}
				for d in fyts_divs:
					fyts_name = d.find('div',attrs={'class':'name'}).getText()
					fyts_content = d.find('div',attrs={'class':'content'}).getText().strip()
					fyts_dict[fyts_name] = fyts_content
				for i in fyts_name_dict.keys():
					if i in fyts_dict.keys():
						item[fyts_name_dict[i]] = fyts_dict[i]
					else:
						item[fyts_name_dict[i]] = ''
			except:
				for i in fyts_name_dict.values():
					item[i] = ''
				item['fangyuanbiaoqian'] = ''
			try:
				fzzj_div = soup.find('div',attrs={'class':'newwrap yezhuSell'})
				item['fangzhuzijian'] = fzzj_div.find('div',attrs={'class':'txt'}).getText().strip()
			except:
				item['fangzhuzijian'] = ''
			yield item


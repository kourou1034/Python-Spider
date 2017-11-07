import scrapy
from lianjia.items import LianjiaItem
from bs4 import BeautifulSoup
import time
import requests

class HouseSpider(scrapy.Spider):
	name = 'lianjia_zaishou_nanjing'
	allowed_domains = ['nj.lianjia.com/']
	start_urls = ['https://nj.lianjia.com/ershoufang/gulou/',
	'https://nj.lianjia.com/ershoufang/jianye/',
	'https://nj.lianjia.com/ershoufang/qinhuai/',
	'https://nj.lianjia.com/ershoufang/xuanwu/',
	'https://nj.lianjia.com/ershoufang/yuhuatai/',
	'https://nj.lianjia.com/ershoufang/qixia/',
	'https://nj.lianjia.com/ershoufang/jiangning/',
	'https://nj.lianjia.com/ershoufang/pukou/',
	'https://nj.lianjia.com/ershoufang/liuhe/',
	'https://nj.lianjia.com/ershoufang/lishui/']
	'''
	鼓楼：https://bj.lianjia.com/chengjiao/gulou/
	建邺：https://bj.lianjia.com/chengjiao/jianye/
	秦淮：https://bj.lianjia.com/chengjiao/qinhuai/
	玄武：https://bj.lianjia.com/chengjiao/xuanwu/
	雨花台：https://bj.lianjia.com/chengjiao/yuhuatai/
	栖霞：https://bj.lianjia.com/chengjiao/qixia/
	江宁：https://bj.lianjia.com/chengjiao/jiangning/
	浦口：https://bj.lianjia.com/chengjiao/pukou/
	六合：https://bj.lianjia.com/chengjiao/liuhe/
	溧水：https://bj.lianjia.com/chengjiao/lishui/
	高淳：https://bj.lianjia.com/chengjiao/gaochun/
	'''

	# def parse(self, response):
	# 	# 获取每个区里各个街道的url，然后跳转到街道页面
	# 	data = response.body
	# 	soup = BeautifulSoup(data, 'lxml')
	# 	div_ershoufang_jiedao = soup.find('div', attrs={'data-role':'ershoufang'}).find_all('div')[1]
	# 	a_lists = div_ershoufang_jiedao.find_all('a')
	# 	for a in a_lists:
	# 		area_href = a['href']
	# 		area_url = 'https://nj.lianjia.com' + area_href
	# 		jiedao_name = a.getText()

	# 		yield scrapy.Request(url = area_url,meta={'item1':area_href},callback=self.area_parse,dont_filter=True)

	def parse(self,response):
		data = response.body
		soup = BeautifulSoup(data,'lxml')
		area_href = response.url
		for i in range(1,4):
			try:
				for n in range(1,60):
					try:
						page_url = area_href+'pg'+str(n)+'lc'+str(i)+'/'
						yield scrapy.Request(page_url, callback=self.get_house_url, dont_filter=True)
					except:
						break
			except:
				pass


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


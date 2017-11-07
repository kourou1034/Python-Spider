import scrapy
from lianjia.items import LianjiaItem
from bs4 import BeautifulSoup
import time
import requests

class HouseSpider(scrapy.Spider):
	name = 'lianjia_chengjiao_beijing'
	allowed_domains = ['lf.lianjia.com/']
	start_urls = ['https://lf.lianjia.com/chengjiao/yanjiao/',
	'https://lf.lianjia.com/chengjiao/xianghe/']
	'''
	东城：https://bj.lianjia.com/chengjiao/dongcheng/
	西城：https://bj.lianjia.com/chengjiao/xicheng/
	朝阳：https://bj.lianjia.com/chengjiao/chaoyang/
	海淀：https://bj.lianjia.com/chengjiao/haidian/
	丰台：https://bj.lianjia.com/chengjiao/fengtai/
	石景山：https://bj.lianjia.com/chengjiao/shijingshan/
	通州：https://bj.lianjia.com/chengjiao/tongzhou/
	昌平：https://bj.lianjia.com/chengjiao/changping/
	大兴：https://bj.lianjia.com/chengjiao/daxing/
	亦庄开发区：https://bj.lianjia.com/chengjiao/yizhuangkaifaqu/
	顺义：https://bj.lianjia.com/chengjiao/shunyi/
	房山：https://bj.lianjia.com/chengjiao/fangshan/
	门头沟：https://bj.lianjia.com/chengjiao/mentougou/
	平谷：https://bj.lianjia.com/chengjiao/pinggu/
	怀柔：https://bj.lianjia.com/chengjiao/huairou/
	密云：https://bj.lianjia.com/chengjiao/miyun/
	延庆：https://bj.lianjia.com/chengjiao/yanqing/
	燕郊：https://lf.lianjia.com/chengjiao/yanjiao/
	香河：https://lf.lianjia.com/chengjiao/xianghe/
	'''

	def parse(self, response):
		# 获取每个区里各个街道的url，然后跳转到街道页面
		data = response.body
		soup = BeautifulSoup(data, 'lxml')
		div_ershoufang_jiedao = soup.find('div', attrs={'data-role':'ershoufang'}).find_all('div')[1]
		a_lists = div_ershoufang_jiedao.find_all('a')
		for a in a_lists:
			area_href = a['href']
			area_url = 'https://lf.lianjia.com' + area_href
			jiedao_name = a.getText()

			yield scrapy.Request(url = area_url,meta={'item1':area_href},callback=self.area_parse,dont_filter=True)

	def area_parse(self,response):
		data = response.body
		soup = BeautifulSoup(data,'lxml')
		area_href = response.meta['item1']
		for i in range(1,6):
			try:
				for n in range(1,101):
					try:
						page_url = 'https://lf.lianjia.com'+area_href+'pg'+str(n)+'lc'+str(i)+'/'
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
		ul_ershoufang_house = soup.find('ul',attrs={'class':'listContent'})
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
			item['qu'] = soup.find('div', attrs={'class':'deal-bread'}).find_all('a')[2].getText()[:-7]
			item['jiedao'] = soup.find('div', attrs={'class':'deal-bread'}).find_all('a')[3].getText()[:-7]
			title = soup.find('div',attrs={'class':'wrapper'}).find('h1').getText()
			title_split = title.split(' ')
			item['name'] = title_split[0]
			item['houseArea'] = title_split[2]
			item['dealTime'] = soup.find('div',attrs={'class':'wrapper'}).find('span').getText().split(' ')[0]
			item['jiaoyipingtai'] = soup.find('div',attrs={'class':'wrapper'}).find('span').getText().split(' ')[1]
			try:
				item['totalPrice'] = soup.find('div', attrs={'class':'price'}).find('i').getText()
			except:
				item['totalPrice'] = 0
			try:
				item['unitPrice'] = soup.find('div', attrs={'class':'price'}).find('b').getText()
			except:
				item['unitPrice'] = 0
			try:	
				item['initPrice'] = soup.find('div',attrs={'class':'info fr'}).find('div', attrs={'class':'msg'}).find_all('span')[0].find('label').getText()
			except:
				item['initPrice'] = 0
			base_lists = soup.find('div', attrs={'class':'base'}).find('div', attrs={'class':'content'}).find_all('li')
			item['jishijiting'] = base_lists[0].getText().strip('房屋户型').strip()
			item['houseFloor'] = base_lists[1].getText().strip('所在楼层').strip()
			item['jianzhumianji'] = base_lists[2].getText().strip('建筑面积').strip()
			item['huxingjiegou'] = base_lists[3].getText().strip('户型结构').strip()
			item['taoneimianji'] = base_lists[4].getText().strip('套内面积').strip()
			item['buildingType'] = base_lists[5].getText().strip('建筑类型').strip()
			item['houseOrientation'] = base_lists[6].getText().strip('房屋朝向').strip()
			item['houseDate'] = base_lists[7].getText().strip('建成年代').strip()
			item['Decoration'] = base_lists[8].getText().strip('装修情况').strip()
			item['jianzhujiegou'] = base_lists[9].getText().strip('建筑结构').strip()
			item['gongnuanfangshi'] = base_lists[10].getText().strip('供暖方式').strip()
			item['tihubili'] = base_lists[11].getText().strip('梯户比例').strip()
			item['chanquannianxian'] = base_lists[12].getText().strip('产权年限').strip()
			item['ladder'] = base_lists[13].getText().strip('配备电梯').strip()
			jiaoyi_lists = soup.find('div', attrs={'class':'transaction'}).find_all('li')
			item['fangwuyongtu'] = jiaoyi_lists[3].getText().strip('房屋用途').strip()
			item['fangwunianxian'] = jiaoyi_lists[4].getText().strip('房屋年限').strip()
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


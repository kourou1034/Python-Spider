import scrapy
from weibo.items import WeiboItem
import json
import numpy as np

class WeiboSpider(scrapy.Spider):
	name = 'weibo'
	allowed_domains = ['m.weibo.cn']
	start_urls = ['https://m.weibo.cn/status/4070116385690289',]

	def parse(self, response):
		print('爬虫开始。。')
		start_page = 2815
		end_page = 2850
		for i in range(start_page, end_page):
			try:
				com_url = 'http://m.weibo.cn/api/comments/show?id=4070116385690289&page=' + str(i)
				yield scrapy.Request(url=com_url, callback=self.parse_com, dont_filter=True)
			except:
				print('error........................')
				continue

	def parse_com(self, response):
		title_code = '%25E5%259F%25BA%25E6%259C%25AC%25E4%25BF%25A1%25E6%2581%25AF'
		featurecode = 20000180
		dictCom = json.loads(response.body_as_unicode())
		lisCom = dictCom['data']
		for li in lisCom:
			item1 = {}
			cid = li['id']
			uid = li['user']['id']
			source = li['source']
			text = li['text']
			time = li['created_at']
			containorid = int('230283' + str(uid))
			lfid = int('230283' + str(uid))
			item1['cid'] = cid
			item1['uid'] = uid
			item1['source'] = source
			item1['text'] = text
			item1['time'] = time
			profile_url = 'http://m.weibo.cn/api/container/getIndex?containerid='+str(containorid)+'_-_INFO&title='+str(title_code)+'&luicode=10000011&lfid='+str(lfid)+'&featurecode='+str(featurecode)
			print(profile_url)
			yield scrapy.Request(url=profile_url, meta={'item':item1}, callback=self.parse_fans, dont_filter=True)

	def parse_fans(self, response):
		item2 = response.meta['item']
		item = WeiboItem()
		profile_dic = json.loads(response.body_as_unicode())
		fans_lis = profile_dic['cards'][0]['card_group']
		temp_item = []
		a = {'昵称':[], '性别':[], '所在地':[], '简介':[]}
		b = {'注册时间':[]}
		for l in fans_lis:
			if 'item_name' in l.keys() and l['item_name'] != '标签':
				a[l['item_name']] = l['item_content']
				temp_item.append(l['item_name'])
		if '性别' not in temp_item:
			a['性别'] = np.nan

		for li in profile_dic['cards']:
			fans_lis = li['card_group']
			for dic in fans_lis:
				if '注册时间' in dic.values():
					b['注册时间'] = dic['item_content']
					break
		if b['注册时间'] == '':
			b['注册时间'] = np.nan

		item['cid'] = item2['cid']
		item['uid'] = item2['uid']
		item['source'] = item2['source']
		item['text'] = item2['text']
		item['time'] = item2['time']
		item['name'] = a['昵称']
		item['sex'] = a['性别']
		item['location'] = a['所在地']
		item['intro'] = a['简介']
		# item['level'] = b['等级']
		item['regi_date'] = b['注册时间']
		# item['credit'] = b['阳光信用']

		yield item
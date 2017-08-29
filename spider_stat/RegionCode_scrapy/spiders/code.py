import scrapy
from RegionCode.items import RegioncodeItem
from bs4 import BeautifulSoup

class CodeSpider(scrapy.Spider):
	name = 'RegionCode'
	allowed_domains = ["stats.gov.cn"]
	start_urls = ["http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2016/41.html",]

	# def parse(self, response):
	# 	print(response.url)
	# 	province_tds = response.xpath('//tr[@class="provincetr"]//td')
	# 	item = RegioncodeItem()
	# 	for td in province_tds:
	# 		pro_url_tail = td.xpath('a/@href')[0].extract()
	# 		pro_name = td.xpath('a/text()')[0].extract()
	# 		item['code'] = pro_url_tail[:-5]
	# 		item['name'] = pro_name
	# 		yield item


	# 		pro_url = 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2016/' + pro_url_tail
	# 		yield scrapy.Request(url=pro_url, callback=self.parse_province, dont_filter=True)

	def parse(self, response):
		print(response.url)
		data = response.body
		soup = BeautifulSoup(data, 'lxml')
		citytrs = soup.find_all('tr', attrs={'class':'citytr'})
		item = RegioncodeItem()
		for ctr in citytrs:
			citytds = ctr.find_all('td')
			city_url_tail = citytds[0].find('a')['href']
			city_name = citytds[1].getText()
			city_code = citytds[0].getText()
			item['code'] = city_code
			item['name'] =city_name
			yield item

			city_url = 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2016/' + city_url_tail
			yield scrapy.Request(city_url, callback=self.parse_city)

	def parse_city(self, response):
		print(response.url)
		item = RegioncodeItem()
		data = response.body
		soup = BeautifulSoup(data, 'lxml')
		countytrs = soup.find_all('tr', attrs={'class':'countytr'})
		for countytr in countytrs:
			link = countytr.find_all('a')
			if len(link) == 0:
				tds = countytr.find_all('td')
				county_code = tds[0].getText()
				county_name = tds[1].getText()
				item['code'] = county_code
				item['name'] = county_name
				yield item
			else:
				county_url_tail = link[0]['href']
				tds = countytr.find_all('td')
				county_code = tds[0].getText()
				county_name = tds[1].getText()
				item['code'] = county_code
				item['name'] = county_name
				yield item

				county_url = response.url[:-9] + county_url_tail
				yield scrapy.Request(county_url, callback=self.parse_county)

	def parse_county(self, response):
		print(response.url)
		item = RegioncodeItem()
		data = response.body
		soup = BeautifulSoup(data, 'lxml')
		towntrs = soup.find_all('tr', attrs={'class':'towntr'})
		for ttr in towntrs:
			tds = ttr.find_all('td')
			town_code = tds[0].getText()
			town_name = tds[1].getText()
			link = ttr.find_all('a')[0]['href']
			item['code'] = town_code
			item['name'] = town_name
			yield item

			town_url = response.url[:-11] + link
			yield scrapy.Request(town_url, callback=self.parse_town)

	def parse_town(self, response):
		print(response.url)
		item = RegioncodeItem()
		data = response.body
		soup = BeautifulSoup(data, 'lxml')
		nctrs = soup.find_all('tr', attrs={'class':'villagetr'})
		for nctr in nctrs:
			tds = nctr.find_all('td')
			nc_code = tds[0].getText()
			nc_name = tds[2].getText()
			item['code'] = nc_code
			item['name'] = nc_name
			yield item

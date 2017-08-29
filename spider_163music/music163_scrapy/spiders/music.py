import scrapy
from music163.items import Music163Item
from selenium import webdriver
from scrapy.selector import HtmlXPathSelector

class MusicSpider(scrapy.Spider):
	name = 'Music163'
	allowed_domains = ["music.163.com"]
	start_urls = ["http://music.163.com/discover/artist",]

	def parse(self, response):
		print(response.url)
		print("正在爬取推荐歌手...")
		artists = response.xpath('//*[@id="m-artist-box"]/li')
		print(artists)
		for li in artists:
			artist_url = li.xpath('//a[@class="nm nm-icn f-thide s-fc0"]/@href')[0].extract()
			new_url = 'http://music.163.com' + str(artists)

			yield scrapy.Request(url=new_url, callback=self.parse_artist, dont_filter=True)

	def parse_artist(self, response):
		item = Music163Item()
		artist_name = response.xpath('//*[@id="artist-name"]/text()')[0].extract()
		print(artist_name)
		item['artist'] = artist_name
		print("正在爬取热门歌曲...")
		songs = response.xpath('//table[@id="auto-id-dqeTzu51W1gZO0rw"]/tbody/tr[@class="even"]')
		for tr in songs:
			song_url = tr.xpath('//div[@class="f-cb"]/a/@href')[0].extract(			print(song_name)
			item['song'] = song_name
			new_url2 = 'http://music.163.com' + str(song_url)

			yield scrapy.Request(url=new_url2, meta={'item':item}, callback=self.parse_song)

	def parse_song(self, response):
		item = response.meta['item']
		item['url'] = response.url
		item['comment'] = response.xpath('//*[@id="comment-box"]//span[@class="j-flag"]/text()')[0].extract()

		yield item
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  5 13:00:41 2017

@author: ThinkPad
"""

import scrapy
from hupu.items import HupuItem


class HupuSpider(scrapy.Spider):
    name = 'hupu'
    allowed_domains = ["bbs.hupu.com"]
    start_urls = ('https://bbs.hupu.com/bxj',)
    

    
#    def start_requests(self):
#        reqs1=[]
#        for i in range(1, 10):
#            req=scrapy.Request("https://bbs.hupu.com/bxj-%s" %i)
#            reqs1.append(req)
#        return reqs1
        
    def parse(self, response):
        trs = response.xpath('//*[@id="pl"]/tbody[1]/tr')
        for tr in trs:
            item = HupuItem()
            item['author'] = tr.xpath('td[@class="p_author"]/a/text()')[0].extract()
            item['time'] = tr.xpath('td[@class="p_retime"]/a/text()')[0].extract()
            url = tr.xpath('td[@class="p_title"]/a/@href')[0].extract()
            item['url'] = url if "https:" in url else ("https://bbs.hupu.com" + url)
            
            yield scrapy.Request(url=item['url'], meta={'item':item},callback=self.parse_detail)
    
    def parse_detail(self, response):
        
        item = response.meta['item']
        item['title'] = response.xpath('//div[@class="subhead"]/span/text()')[0].extract()
        item['artical'] = response.xpath('//div[@id="tpc"]//div[@class="quote-content"]/div/text()').extract()
    
        yield item

# -*- coding: utf-8 -*-
"""
Created on Sun Aug 13 10:17:43 2017

@author: ThinkPad
"""

import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook
import time

wb = Workbook()
ws = wb.active
line = ['name','code']
ws.append(line)

def parser_page(url):
    header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'}
    data = requests.get(url, headers=header).content
    soup = BeautifulSoup(data, 'lxml')
    return soup

    
start_url = 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2016/index.html'
url_head = 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2016/'
index_soup = parser_page(start_url)
province_trs = index_soup.find_all('tr', attrs={'class':'provincetr'})

for protr in province_trs:
    province_tds = protr.find_all('td')
    for protd in province_tds:
        pro_name = protd.getText()
        url_tail = protd.find('a')['href']
        pro_name = protd.find('a').getText().strip()
        province_url = url_head + url_tail
        print(pro_name, url_tail)
        
        province_soup = parser_page(province_url)
        citytrs = province_soup.find_all('tr', attrs={'class':'citytr'})
        for ctr in citytrs:
            citytds = ctr.find_all('td')
            code = citytds[0].getText()
            name = citytds[1].getText()
            city_url_tail = citytds[0].find('a')['href']
            print(name, code)
            line = [code, name]
            ws.append(line)
            city_url = url_head + city_url_tail
            city_soup = parser_page(city_url)
            countytrs = city_soup.find_all('tr', attrs={'class':'countytr'})
            for countytr in countytrs:
                link = countytr.find_all('a')
                if len(link) == 0:
                    tds = countytr.find_all('td')
                    code = tds[0].getText()
                    name = tds[1].getText()
                    print(name,code)
                    line = [code, name]
                    ws.append(line)
                else:
                    county_url_tail = link[0]['href']
                    tds = countytr.find_all('td')
                    code = tds[0].getText()
                    name = tds[1].getText()
                    print(name,code)
                    line = [code, name]
                    ws.append(line)
                    county_url = city_url[:-9] + county_url_tail
                    county_soup = parser_page(county_url)
                    towntrs = county_soup.find_all('tr', attrs={'class':'towntr'})
                    for ttr in towntrs:
                        tds = ttr.find_all('td')
                        code = tds[0].getText()
                        name = tds[1].getText()
                        link = ttr.find_all('a')[0]['href']
                        print(name, code)
                        line = [code, name]
                        ws.append(line)
                        town_url = county_url[:-11] + link
                        town_soup = parser_page(town_url)
                        nctrs = town_soup.find_all('tr', attrs={'class':'villagetr'})
                        for nctr in nctrs:
                            tds = nctr.find_all('td')
                            code = tds[0].getText()
                            name = tds[2].getText()
                            print(name, code)
                            line = [code, name]
                            ws.append(line)
        time.sleep(2)
             
wb.save('C:\\Users\\Think\\desktop\\code.xlsx')
                        
                    
                    
                    

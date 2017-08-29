# -*- coding: utf-8 -*-
"""
Created on Sun Jun 25 08:52:32 2017

@author: ThinkPad
"""

import json
import numpy as np
import requests
from openpyxl import Workbook
from datetime import datetime
#from bs4 import BeautifulSoup
#import socket

def crawler(comment_url, headers, ws, proxies):    
    title_code = '%25E5%259F%25BA%25E6%259C%25AC%25E4%25BF%25A1%25E6%2581%25AF'
    featurecode = 20000180
    
    #data = requests.get(comment_url, headers=headers, proxies=proxies).content
    data = requests.get(comment_url, headers=headers).content
    dictCom = json.loads(data)
    lisCom = dictCom['data']
    count = 1
    
    for li in lisCom:
        try:
            print('获取第%s条评论信息...' %count)
            cid = li['id']
            uid = li['user']['id']
            source = li['source']
            text = li['text']
            times = li['created_at']
            containorid = int('230283' + str(uid))
            lfid = int('230283' + str(uid))
            profile_url = 'http://m.weibo.cn/api/container/getIndex?containerid=%s_-_INFO&title=%s&luicode=10000011&lfid=%s&featurecode=%s'%(containorid,title_code,lfid,featurecode)
            
            #data1 = requests.get(profile_url, headers=headers, proxies=proxies).content
            data1 = requests.get(profile_url, headers=headers).content
            profile_dic = json.loads(data1)
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
            line = [cid,uid,text,source,times,a['性别'],a['昵称'],a['所在地'],a['简介'],b['注册时间']]
            ws.append(line)
            count += 1
        except Exception as e:
            print(e)
            continue


def get_proxies():
    
    # 要访问的目标页面
    # targetUrl = "http://test.abuyun.com/proxy.php"
    # targetUrl = "http://proxy.abuyun.com/switch-ip"
    # targetUrl = "http://proxy.abuyun.com/current-ip"
    # 代理服务器
    proxyHost = "proxy.abuyun.com"
    proxyPort = "9010"
    # 代理隧道验证信息
    proxyUser = "H17A4HIEJ5P2A29P"
    proxyPass = "9F0D1E3600AA19F3"
    proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
      "host" : proxyHost,
      "port" : proxyPort,
      "user" : proxyUser,
      "pass" : proxyPass,
    }
    
    proxies = {
        "http"  : proxyMeta,
        "https" : proxyMeta,
    }
    
    return proxies

        
def main():
    now = datetime.now()
    print(now)
    cookie = '_T_WM=c3b29c1a8e5b07c36e699dfb23cef041; ALF=1500900286; SCF=AjDMmGAmOMk0ZfasvNuMW8wD8NOxPhO5cMqOWP5ddiVNNSgFur3VkVaOfm1-hFtItjX0SSbSFagrihioi4mhdjs.; SUB=_2A250Si7uDeRhGedH7VcY9ynPyz-IHXVXtLKmrDV6PUNbktBeLWOkkW097ZLzN4uOCN8QrKNSpWT2SoLBKw..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WW4J5ic6pA5nczWpHyFwDXN5JpX5KMhUgL.Fo24So-4S0M0ehe2dJLoIX5LxKqL1hnL1K2LxKqL1hBLB.qLxK-L1heL12qLxKBLBonL1h5LxK-L1-BL1KMLxKqL1h.LBKeLxKnL1hzL1hLu; SUHB=00xoidcbLtY0w6; M_WEIBOCN_PARAMS=featurecode%3D20000320%26luicode%3D20000174%26lfid%3Dhotword'
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36', 'Cookie':cookie}
    start_page = 2647
    end_page = 2970
    wb = Workbook()
    ws = wb.active
    # proxy_url = 'http://www.xicidaili.com/nn/1'
    # useful_proxies =   get_proxy(url=proxy_url, headers=headers)
    #proxies = get_proxies()
    proxies = []
    for p in range(start_page, end_page):
        try:
            # proxy = np.random.choice(useful_proxies)
            comment_url = 'http://m.weibo.cn/api/comments/show?id=4070116385690289&page=%s'%p
            print('now to get  ' + comment_url)
            crawler(comment_url, headers, ws, proxies)
        except Exception as e:
            print(e)
            continue

    wb.save('C:\\Users\\Think\\desktop\\weibo\\624-5.xlsx') 
    
    end = datetime.now()
    print(end)
    print('程序耗时：'+str(end-now))

    
if __name__ == '__main__':
    main()
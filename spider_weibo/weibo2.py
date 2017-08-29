# -*- coding: utf-8 -*-
"""
Created on Wed Jun 21 08:33:46 2017

@author: ThinkPad
"""

import urllib.request
import urllib
import json
# import pandas as pd
import numpy as np
import requests
from openpyxl import Workbook
import threading
# import codecs
from datetime import datetime
import time

def crawler(comment_url, headers, ws):
    
    #start_url = 'http://m.weibo.cn/status/4070116385690289'
    
    title_code = '%25E5%259F%25BA%25E6%259C%25AC%25E4%25BF%25A1%25E6%2581%25AF'
    featurecode = 20000180
    

    data = requests.get(comment_url, headers=headers).content
    dictCom = json.loads(data)
    lisCom = dictCom['data']

    for li in lisCom:
#            print('获取第%s条评论信息...' %count)
        uid = li['user']['id']
        source = li['source']
        text = li['text']
        times = li['created_at']
        containorid = int('230283' + str(uid))
        lfid = int('230283' + str(uid))
        profile_url = 'http://m.weibo.cn/api/container/getIndex?containerid=%s_-_INFO&title=%s&luicode=10000011&lfid=%s&featurecode=%s'%(containorid,title_code,lfid,featurecode)
        
#        request = urllib.request.Request(profile_url, headers=headers)
#        data1 = urllib.request.urlopen(request).read()
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
        line = [uid,text,source,times,a['性别'],a['昵称'],a['所在地'],a['简介'],b['注册时间']]
        ws.append(line)


def main():
    now = datetime.now()
    print(now)
    cookie = '_T_WM=c3b29c1a8e5b07c36e699dfb23cef041; ALF=1500900286; SCF=AjDMmGAmOMk0ZfasvNuMW8wD8NOxPhO5cMqOWP5ddiVNNSgFur3VkVaOfm1-hFtItjX0SSbSFagrihioi4mhdjs.; SUB=_2A250Si7uDeRhGedH7VcY9ynPyz-IHXVXtLKmrDV6PUNbktBeLWOkkW097ZLzN4uOCN8QrKNSpWT2SoLBKw..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WW4J5ic6pA5nczWpHyFwDXN5JpX5KMhUgL.Fo24So-4S0M0ehe2dJLoIX5LxKqL1hnL1K2LxKqL1hBLB.qLxK-L1heL12qLxKBLBonL1h5LxK-L1-BL1KMLxKqL1h.LBKeLxKnL1hzL1hLu; SUHB=00xoidcbLtY0w6; SSOLoginState=1498308287; M_WEIBOCN_PARAMS=luicode%3D20000174%26uicode%3D20000174%26featurecode%3D20000320%26fid%3Dhotword'
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36', 'Cookie':cookie}
    
    start_page = 1
    end_page = 21
    wb = Workbook()
    ws = wb.active
    thread = []
    for p in range(start_page, end_page):
        comment_url = 'http://m.weibo.cn/api/comments/show?id=4070116385690289&page=%s'%p
        print('now to get  ' + comment_url)
        t = threading.Thread(target=crawler, args=(comment_url, headers, ws))
        thread.append(t)
#        except:
#            print('unknown error happened...问题不大！')
#            continue
    for j in range(0,20):
        thread[j].start()
        print('start')

    for j in range(0,20):
        thread[j].join()
        print('join')
        
    #time.sleep(10)

    wb.save('C:\\Users\\Think\\desktop\\weibo2.xlsx') 
    
    end = datetime.now()
    print(end)
    print('程序耗时：'+str(end-now))

    
if __name__ == '__main__':
    main()

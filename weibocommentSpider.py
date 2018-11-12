# 原代码参考https://github.com/dataabc/weiboSpider －－ 更新新浪微博api cookie的指南
#-*- coding = utf-8

from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import re
import requests
import pandas   # 没接触pandas之前，一条一条的往csv里写……
import time
import random
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import xlwt
import os

if not os.path.exists('./Data'):
    os.mkdir('./Data')

def get_one_page(url):
    html = requests.get(url,cookies = cookies)
    html_return = html.json()['data']['html']  # html.text无返回，说明不是text格式的
    # print(html_return)
    return html_return

def parse_one_page(html_return):
    pattern = re.compile(r'com.(\d+)"><img alt="(.+?)" src="(.+?)" usercard="(.+?)"></a>.*?</a>：(.+?)</div>',re.S)
    data = re.findall(pattern,html_return)
    # print(data)
    # print(type(data))
    return data
 
def write_to_file(data):
    data_to_write = pandas.DataFrame(data)
    data_to_write.to_csv('test.csv',header = False,index = False,mode = 'a+', encoding="utf_8_sig") # 去掉表头行和索引列, 适配中文
 
def main(i,count):
    # commenturl = 'https://weibo.com/aj/v6/comment/big?ajwvr=6&id='+str(weiboID)+'&page=1&filter=hot&filter_tips_before=0&from=singleWeiBo'
    commenturl = 'https://weibo.com/aj/v6/comment/big?ajwvr=6&id='+str(weiboID_list[count])+'&page='+str(i)+'&filter=hot&filter_tips_before=0&from=singleWeiBo'
    print("found a page" + commenturl)
    html_return = get_one_page(commenturl)                                           # 去掉了不必要的参数后的url
    data = parse_one_page(html_return)
    write_to_file(data)

# To get weibo content's single ID first, (not UID)
# and store every comment to a file

for page_num in range(4,5):
    browser = webdriver.Chrome(executable_path='/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/selenium/chromedriver/chromedriver')
    url = 'https://weibo.com/p/aj/v6/mblog/mbloglist?ajwvr=6&domain=100606&is_all=1&pagebar=1&pl_name=Pl_Official_MyProfileFeed__20&id=1006062168096235&script_uri=/jddjdwewin&feed_type=0&page={}&pre_page={}'.format(page_num,page_num)
    browser.get(url)
    print('Waiting')
    time.sleep(10)
    print('Finish Waiting')

    get_page_source = browser.page_source
    # print(get_page_source)
    soup = BeautifulSoup(get_page_source,"lxml")
    body_text = soup.select('pre')[0]
    bodytext1 = body_text.string
    weiboIDs=bodytext1.split('tbinfo',15)[1:20] #按照tbinfo为分界

    weiboID_list =[]
    for x in weiboIDs:
    	weiboID = x[74:90] #取出每条微博id（16个字符）
    	if weiboID.isdigit():
    		print(weiboID)
    		weiboID_list.append(weiboID)
    	else:
    		pass

    # input each ID to retrieve comment info ###

# weiboID = 4287745293901676


# headers = {'User-Agent': UserAgent().random}
 
cookies = {"Cookie": "ALF=1541678599; _T_WM=c5a6e5105ea72496e25b6f2ee97fe7c5; WEIBOCN_FROM=1110006030; SCF=Alkk5kDTOrqwof630yIp5H3MU-xEEzAe_dhHdbkkP6c7j3cCuQwnz-CwnZvWLUcI5RrSkOmknLD5qqye09RlXwQ.; SUB=_2A252uO0gDeRhGeBI7VcR-S7PyzSIHXVSQvNorDV6PUJbktAKLRaskW1NRm9icCRrm32y5Dsn88GtxJMQCpBtYqZD; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWdX4fWF0BUXpOlaZOE.Eb75JpX5K-hUgL.FoqcSo-71K50ehn2dJLoIEXLxKML1K2L1--LxKMLBKML12zLxKBLBonL12zLxK.L1-zLBKnLxK-LBKBLBK.t; SUHB=0A0JbHNN94JiCR; SSOLoginState=1539087728"}  # 将your cookie替换成自己的cookie

if __name__=='__main__':
    totalcomment = len(weiboID_list)
    for count in range(0,totalcomment): #这个list中的每一个微博
        for i in range(1,2): #每个微博的top20评论
            main(i,count) 
        print("weibo No."+str(count))  
        time.sleep(random.uniform(2,6))      

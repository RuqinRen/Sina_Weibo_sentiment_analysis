from aip import AipNlp
import csv
import pandas
import time
import random

""" 你的 APPID AK SK """
APP_ID = 'XXX'
API_KEY = 'XXX'
SECRET_KEY = 'XXX'

client = AipNlp(APP_ID, API_KEY, SECRET_KEY)

def is_chinese(uchar):
    """判断一个unicode是否是汉字"""
    if uchar >= u'\u4e00' and uchar <= u'\u9fa5':
        return True
    else:
        return False

def format_str(content):
    content_str = ''
    for i in content:
        if is_chinese(i):
            content_str = content_str+i
    return content_str  

def write_to_file(data):
    data_to_write = pandas.DataFrame(data)
    data_to_write.to_csv('test.csv',header = False,index = False,mode = 'a+', encoding="utf_8_sig") # 去掉表头行和索引列, 适配中文

options13 = {}
options13["type"] = 13 #13 is for 3C products, or 11 for Life-related 

options11 = {}
options11["type"] = 11 #13 is for 3C products, or 11 for Life-related 


line_count=0
# with open('XXX.csv') as csv_file:
#     csv_reader = csv.reader(csv_file, delimiter=',',nrows=3)
    # csv_reader.read_csv('1faceu.csv', skiprows=0, nrows=10)
df = pandas.read_csv('XXXXX.csv', delimiter=',')
alldata=[]
for eachrow in df.loc[149:220].values: #choose first 150 rows 为了容错
    # print(eachrow)
    data={}
    if line_count < 700:
        onlyCN_text = format_str(eachrow[-1])
        # print(onlyCN_text)
        if onlyCN_text:
            data['aonlyCN_text'] = onlyCN_text

            sentiment_result = client.sentimentClassify(onlyCN_text)
            result = sentiment_result['items'][-1]
            data['bpositive_score'] = result['positive_prob']
            data['cnegative_score'] = result['negative_prob']
            data['dsentiment_score'] = result['sentiment']
            data['econfidence_int'] = result['confidence']

            time.sleep(random.uniform(1,7))

            result2 = client.commentTag(onlyCN_text,options13)
            if result2.__contains__('items'):
                data['felectronic_type'] = result2['items'][-1]['prop']
            else:
                pass

            result3= client.commentTag(onlyCN_text,options11)
            if result3.__contains__('items'):
                data['glife_type'] = result3['items'][-1]['prop']
            else:
                pass
            # data=onlyCN_text,positive_score,negative_score,sentiment_score,confidence_int,electronic_type,life_type)
            print(data)
            print('running row'+str(line_count))
            line_count +=1
            with open('test.csv', 'a') as f:  # Just use 'w' mode in 3.x
                w = csv.DictWriter(f, data.keys())
                w.writerow(data)
    else:
        break



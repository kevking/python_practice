import requests
from requests.exceptions import RequestException
import re
import os
import pymongo

DB_URL = "localhost"
DB = "my"
TABLE = "my"
client = pymongo.MongoClient(DB_URL,connect=False)
db = client[DB]


header = {
    "Connection": "keep-alive",
    "Referer": "http://maoyan.com/board/4",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/5"
}
def open_web(url):
    try:
        response = requests.get(url,headers = header)
        if(response.status_code == 200):
            return response.text
    except RequestException:
        print('请求失败！')
    return


def fenxi(response):
    pattern = re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?title="(.*?)".*?img src="(.*?)".*?star">(.*?)</p>.*?releasetime">(.*?)</p>.*?integer">(.*?)</i>.*?fraction">(.*?)</i>',re.S)
    resutl = re.findall(pattern,response)
    print(resutl)
    # if resutl:
    #     for rank in resutl:
    #         print(rank[0].strip())#rank
    #         print(rank[1].strip())#name
    #         print(rank[2].strip())#img_url
    #         print(rank[3].strip())#star
    #         print(rank[4].strip())#releasetime
    #         print(rank[5]+rank[6])#score
    #
    # else:
    #     print('没有匹配项')
    return resutl



def save(content):
    path = "e:\\result.txt"
    try:
        with open(path,'a') as f:
            f.write(str(content))
            f.close()
            print("写入成功")
    except Exception as e :
        print("文件写入失败")
        print(e)

def save_mongo(content):
    try:
        for element in content:
            db[TABLE].insert({"rank":element[0],"title":element[1],"src":element[2],"star":element[3].strip(),"time":element[4].strip(),"score":element[5]+element[6]})
            print("success")
    except Exception as e:
        print(e)

def main():
    url = 'http://maoyan.com/board/4?offset='
    for i in range(0,10):
        result = open_web(url + str(i*10))
        save_mongo(fenxi(result))
    return


if __name__ == '__main__':
    main()

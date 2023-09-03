"""
1. 尚未加入資料更新的功能
2. 訊息等級尚需討論
"""

import urllib.request as request
import json
from Main import MongoDB # 引用MongoDB連線實例
from pymongo import InsertOne

def getData():
    """
    一、資料來源: \n
            1. 政府資料開放平臺 - 測速執法設置點 \n
                https://data.gov.tw/dataset/7320
    """
    # 取得資料
    url = "https://od.moi.gov.tw/api/v1/rest/datastore/A01010000C-000674-011"
    data = json.load(request.urlopen(url))
    
    # 將資料整理成MongoDB的格式
    documents = []
    for d in data['result']['records']:
        document = {
            "CityName": d['CityName'],
            'RegionName': d['RegionName'],
            'Address': d['Address'],
            'Longitude': d['Longitude'],
            'Latitude': d['Latitude'],
            'Direct': d['direct'],
            'Limit': d['limit'],
            'MessageLevel': 1
        }
        documents.append(document)

    # 將資料存入MongoDB
    collection = MongoDB.getCollection("TrafficHero","Speed_Enforcement")
    collection.drop()
    collection.insert_many(documents)
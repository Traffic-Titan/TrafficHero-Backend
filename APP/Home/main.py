"""
1. 將各縣市API存進資料庫
2. 讀取資料庫的各個API再分析。
3. 超商因為資料太大，而且沒有附上經緯度座標，需要一個一個寫入。因此仍需要點時間
"""
from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from Service.Token import decode_token
from enum import Enum
import csv
from pydantic import BaseModel
from Service.TDX import getData
from Service.MongoDB import connectDB
from shapely.geometry import Point
from geopy.distance import geodesic
from shapely.geometry.polygon import Polygon
from Service.Google_Maps import geocode
import openpyxl

router = APIRouter(tags=["1.首頁(APP)"],prefix="/Home")

security = HTTPBearer()

"""
1.資料來源:加油站服務資訊
    https://data.gov.tw/dataset/6065
"""
class Gas_Station(BaseModel):
    #CurrentLat:目前緯度 、CurrentLng:目前經度 、Type: 加盟站 or 自營站
    CurrentLat:float
    CurrentLng:float
    Type:str
def get_Gas_Station_LatLng(CurrentLat:str,CurrentLng:str,Type:str):
    
    #Points_After_Output:存半徑 N 公里生成的點、match_Station:存符合資格的站點
    Points_After_Output = []
    match_Station = []
    
    for angle in range(0, 360, 60):
        # 以使用者目前的經緯度查詢 半徑 1 公里 內的加油站
        Points_After_Output.append(geodesic(kilometers=1).destination((CurrentLat, CurrentLng),bearing = angle))

    #讀檔 中油加油站清冊.csv
    with open(r'./APP/Home/中油加油站清冊.csv',encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            try:
                point = Point([float(row[24]), float(row[23])])
                if(Polygon(Points_After_Output).contains(point) and Type == row[1]):
                    match_Station.append(str(row[24])+","+str(row[23]))
            except:
                pass
    return match_Station      

@router.post("/QuickSearch/Gas_Station")
def QuickSearch_Gas_Station(gas:Gas_Station, token: HTTPAuthorizationCredentials = Depends(security)):
    # JWT驗證
    decode_token(token.credentials)
    
    Url = []
    for data in get_Gas_Station_LatLng(gas.CurrentLat,gas.CurrentLng,gas.Type):
        Url.append("https://www.google.com/maps/dir/?api=1&destination="+ data +"&travelmode=driving&dir_action=navigate")
    return Url


class ConvenientStore(BaseModel):
    #CurrentLat:目前緯度 、CurrentLng:目前經度 、Type: 直營or加盟
    CurrentLat:float
    CurrentLng:float
def get_ConvenientStore(CurrentLat:str,CurrentLng:str):
    #Points_After_Output:存半徑 N 公里生成的點、match_Station:存符合資格的站點
    Points_After_Output = []
    match_Station = []
    
    for angle in range(0, 360, 60):
        # 以使用者目前的經緯度查詢 半徑 1 公里 內的便利商店
        Points_After_Output.append(geodesic(kilometers=1).destination((CurrentLat, CurrentLng),bearing = angle))
    
    #讀檔 全國五大超商資料集.csv
    with open(r'./APP/Home/全國5大超商資料集.csv',encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        # writer = csv.writer(csvfile)

        for row in reader:
            try:
                # writer.writerow(geocode(row[4]))
                point = Point([geocode(row[4])])
                if(Polygon(Points_After_Output).contains(point)):
                    match_Station.append(str(row[1]))
            except:
                pass

    return match_Station
    
@router.post("/QuickSearch/ConvenientStore")
def QuickSearch_ConvenientStore(convenient:ConvenientStore, token: HTTPAuthorizationCredentials = Depends(security)):
    # JWT驗證
    decode_token(token.credentials)

    return get_ConvenientStore(convenient.CurrentLat,convenient.CurrentLng)


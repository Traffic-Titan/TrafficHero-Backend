# 暫時性檔案，放Router用
from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import Service.Token as Token
import requests
from Main import MongoDB # 引用MongoDB連線實例
import xml.etree.ElementTree as ET
from Service.TDX import getData
from APP.Information.PublicTransport.PublicBicycle import getBikeStatus
import time

router = APIRouter(tags=["4-2.大眾運輸資訊(APP)"],prefix="/APP/Information/PublicTransport/TaiwanRailway")
@router.get("/DailyTimeTable_ByStartEndStation",summary="【Read】大眾運輸資訊-台鐵指定[日期][起訖站]時刻表查詢")
async def DailyTimeTable_ByStartEndStation(OriginStationID :str,DestinationStationID:str,TrainDate = str,token: HTTPAuthorizationCredentials = Depends(HTTPBearer())):

    """
    一、資料來源: \n
         1.  交通部運輸資料流通服務平臺(TDX) - 指定[日期][起迄站間]之台鐵時刻表資料  \n
        https://tdx.transportdata.tw/api-service/swagger/basic/5fa88b0c-120b-43f1-b188-c379ddb2593d#/TRA/DailyTrainTimeTableApiController_Get_3211_5\n
    二、Input \n
        1. \n
    三、Output \n
        1. 
    四、說明 \n
        1. 欲查詢的日期(格式: yyyy-MM-dd) \n
    """
    Token.verifyToken(token.credentials,"user") # JWT驗證
    documents = []

    DailyTimeTable_URL = f"https://tdx.transportdata.tw/api/basic/v3/Rail/TRA/DailyTrainTimetable/OD/Inclusive/{OriginStationID}/to/{DestinationStationID}/{TrainDate}?%24top=30&%24format=JSON"
    DailyTimeTable_data = getData(DailyTimeTable_URL)
    for data in DailyTimeTable_data['TrainTimetables']:
        document = {
            "TrainNo":data['TrainInfo']['TrainNo'],
            "Direction": data['TrainInfo']["Direction"],
            "TrainTypeName": data['TrainInfo']['TrainTypeName']['Zh_tw'],
            "StartingStationName":data['TrainInfo']["StartingStationName"]['Zh_tw'],
            "EndingStationName":data['TrainInfo']["EndingStationName"]['Zh_tw'],
            "TripLine":data['TrainInfo']['TripLine'],
            "WheelChairFlag": data['TrainInfo']['WheelChairFlag'],
            "PackageServiceFlag":data['TrainInfo']['PackageServiceFlag'],
            "DiningFlag": data['TrainInfo']['DiningFlag'],
            "BreastFeedFlag": data['TrainInfo']['BreastFeedFlag'],
            "BikeFlag": data['TrainInfo']['BikeFlag'],
            "CarFlag": data['TrainInfo']['CarFlag'],
            "DailyFlag": data['TrainInfo']['DailyFlag'],
            "ExtraTrainFlag": data['TrainInfo']['ExtraTrainFlag'],
            "SuspendedFlag":data['TrainInfo']['SuspendedFlag'],
            "StopTimes":data['StopTimes'],
        }
        documents.append(document)
    return documents

@router.get("/DailyTimeTable_ByCarNum",summary="【Read】大眾運輸資訊-台鐵指定[日期][車次]時刻表查詢")
async def DailyTimeTable_ByCarNum(CarNum :str,TrainDate = str,token: HTTPAuthorizationCredentials = Depends(HTTPBearer())):

    """
    一、資料來源: \n
         1.  交通部運輸資料流通服務平臺(TDX) - 指定[日期][車次]之台鐵時刻表資料  \n
        https://tdx.transportdata.tw/api-service/swagger/basic/268fc230-2e04-471b-a728-a726167c1cfc#/TRA/TRAApi_DailyTimetable_2150_4\n
    二、Input \n
        1. \n
    三、Output \n
        1. 
    四、說明 \n
        1. 欲查詢的日期(格式: yyyy-MM-dd) \n
    """
    Token.verifyToken(token.credentials,"user") # JWT驗證
    documents = []

    DailyTimeTable_URL = f"https://tdx.transportdata.tw/api/basic/v2/Rail/TRA/DailyTimetable/TrainNo/{CarNum}/TrainDate/{TrainDate}?%24format=JSON"
    DailyTimeTable_data = getData(DailyTimeTable_URL)
    for data in DailyTimeTable_data:
        document = {
            "TrainNo":data['DailyTrainInfo']['TrainNo'],
            "Direction": data['DailyTrainInfo']["Direction"],
            "TrainTypeName": data['DailyTrainInfo']['TrainTypeName']['Zh_tw'],
            "StartingStationName":data['DailyTrainInfo']["StartingStationName"]['Zh_tw'],
            "EndingStationName":data['DailyTrainInfo']["EndingStationName"]['Zh_tw'],
            "TripLine":data['DailyTrainInfo']['TripLine'],
            "WheelChairFlag": data['DailyTrainInfo']['WheelChairFlag'],
            "PackageServiceFlag":data['DailyTrainInfo']['PackageServiceFlag'],
            "DiningFlag": data['DailyTrainInfo']['DiningFlag'],
            "BreastFeedFlag": data['DailyTrainInfo']['BreastFeedFlag'],
            "BikeFlag": data['DailyTrainInfo']['BikeFlag'],
            "CarFlag": data['DailyTrainInfo']['CarFlag'],
            "DailyFlag": data['DailyTrainInfo']['DailyFlag'],
            "ExtraTrainFlag": data['DailyTrainInfo']['ExtraTrainFlag'],
            "SuspendedFlag":data['DailyTrainInfo']['SuspendedFlag'],
            "StopTimes":data['StopTimes'],
        }
        documents.append(document)
    return documents

@router.get("/DailyTimeTable_ByStation",summary="【Read】大眾運輸資訊-指定臺鐵[車站]定期站別時刻表資料")
async def DailyTimeTable_ByStation(StationID :str,token: HTTPAuthorizationCredentials = Depends(HTTPBearer())):

    """
    一、資料來源: \n
         1.  交通部運輸資料流通服務平臺(TDX) - 指定臺鐵[車站]定期站別時刻表資料  \n
        https://tdx.transportdata.tw/api-service/swagger/basic/5fa88b0c-120b-43f1-b188-c379ddb2593d#/TRA/GeneralStationTimetableApiController_Get_3209_1\n
    二、Input \n
        1. \n
    三、Output \n
        1. 
    四、說明 \n
        1. 欲查詢的日期(格式: yyyy-MM-dd) \n
    """
    Token.verifyToken(token.credentials,"user") # JWT驗證
    documents = []

    DailyTimeTable_URL = f"https://tdx.transportdata.tw/api/basic/v3/Rail/TRA/GeneralStationTimetable/Station/{StationID}?%24format=JSON"
    DailyTimeTable_data = getData(DailyTimeTable_URL)
    for index in DailyTimeTable_data['StationTimetables']:
        for data in index['Timetables']:
            document = {
                "Direction":index['Direction'],
                "TrainNo":data['TrainNo'],
                "DestinationStationName": data["DestinationStationName"]['Zh_tw'],
                "TrainTypeName":data['TrainTypeName']['Zh_tw'],
                "ArrivalTime":data['ArrivalTime'],
                "DepartureTime":data['DepartureTime']
            }
            documents.append(document)
    return documents


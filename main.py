"""
1. 目前設定為每次啟動時，會將資料庫清空，並重新抓取資料，以後必需按照來源狀況，設定更新資料的時間
"""
from fastapi import FastAPI
import os
import datetime
import threading
from dotenv import load_dotenv
import time
from APP.CMS.PBS import getHardShoulder
from apscheduler.schedulers.blocking import BlockingScheduler
import Service.Scheduler as Scheduler

app = FastAPI()

# 外部服務(Dev Only)
from Service import Email_Service, Google_Maps, TDX, Token
app.include_router(Email_Service.router)
app.include_router(Google_Maps.router)
app.include_router(TDX.router)
app.include_router(Token.router)

# 0.會員管理(APP)
from APP.Account import login, register, profile, password, code, SSO
app.include_router(login.router)
app.include_router(register.router)
app.include_router(SSO.router)
app.include_router(password.router)
app.include_router(code.router)
app.include_router(profile.router)

# 0.群組通訊(APP)
from APP.Chat import main
app.include_router(main.router)

# 1.首頁(APP)
from APP.Home import main
app.include_router(main.router)

# 2.最新消息(APP)
from APP.News import main, MRT
app.include_router(main.router)
app.include_router(MRT.router)

# 3.即時訊息推播(APP)
from APP.CMS import main, Speed_Enforcement, Technical_Enforcement,PBS
app.include_router(main.router)

# 4-1.道路資訊(APP)
from APP.Road_Information import main
app.include_router(main.router)

# 4-2.大眾運輸資訊(APP)
from APP.Public_Transport_Information import main
app.include_router(main.router)

# 5.觀光資訊(APP)
from APP.Tourism_Information import main
app.include_router(main.router)

# ---------------------------------------------------------------

# 0.會員管理(Website)
from Website.Account import main
app.include_router(main.router)

# 0.群組通訊(Website)
from Website.Chat import main
app.include_router(main.router)

# 1.首頁(Website)
from Website.Home import main
app.include_router(main.router)

# 2.最新消息(Website)
from Website.News import THSR, MRT, TRA , bus
app.include_router(THSR.router)
app.include_router(MRT.router)
app.include_router(TRA.router)
app.include_router(bus.router)

# 3.即時訊息推播(Website)
from Website.CMS import main
app.include_router(main.router)

# 4-1.道路資訊(Website)
from Website.Road_Information import main
app.include_router(main.router)

# 4-2.大眾運輸資訊(Website)
from Website.Public_Transport_Information import main
app.include_router(main.router)

# 5.觀光資訊(Website)
from Website.Tourism_Information import main
app.include_router(main.router)

# ---------------------------------------------------------------

# 通用功能
from Universal import logo
app.include_router(logo.router)

# ---------------------------------------------------------------

@app.on_event("startup")
async def startup_event():
    load_dotenv()
    # getHardShoulder()
    # Scheduler.start() # 啟動排程
    # setInterval(Speed_Enforcement.getData())
    # setInterval(Technical_Enforcement.getData())
    # setInterval(PBS.getData())
    # Speed_Enforcement.getData()
    # Technical_Enforcement.getData()
    # PBS.getData()

@app.on_event("shutdown")
async def shutdown_event():
    # 在應用程式關閉時斷開連線
    email_server.quit()

#每天0點0分定時執行Function
def setInterval(function):
    #現在時間
    now_time = datetime.datetime.now()

    #明天時間
    next_time = now_time + datetime.timedelta(days=+1)
    next_year = next_time.date().year
    next_month = next_time.date().month
    next_day = next_time.date().day

    #獲取明天0點0分時間
    next_time = datetime.datetime.strptime(str(next_year)+"-"+str(next_month)+"-"+str(next_day)+" 00:00:00","%Y-%m-%d %H:%M:%S")

    #獲取距離明天0點0分的時間 , 單位時間"秒"
    timerStartTime = (next_time - now_time).total_seconds()

    timer = threading.Timer(timerStartTime,function)
    timer.start()
#檢查目前資料庫內的版本與最新的版本有沒有差異，若有的話，通知User更新
# def CheckUpdate_SpeedEnforcement():
#     #連接DataBase
#     # 0715：connectDB()後面的Collection名稱沒辦法當變數
#     Collection = connectDB("Speed_Enforcement")

#     #讀取DataBase內的資料，並存進document
#     document = []
#     count = 0
#     for info in Collection.find({}):
#         document.append(info)
#     #判斷Speed_Enforcement.getData()的經緯度 與 document的經緯度 有無相同。如果全部相同，count應為 2098
#     for speedEnforcement in Speed_Enforcement.getData():
#         for doc in document:
#             if((speedEnforcement['Latitude'],speedEnforcement['Longitude']) == (doc['Latitude'],doc['Longitude'])):
#                 count = count + 1
#     if(count == 2098):
#         print("資料同步")
#     else:
#         print("資料需要更新")
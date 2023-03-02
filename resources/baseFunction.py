import pandas as pd
import datetime
import os
import re
from dateutil.relativedelta import relativedelta


def Get_text(path):
    temp = ''
    if(path):
       with open(path, 'r' ,encoding="utf-8") as file:
          temp = file.read()
    return temp

def Get_text_split(path):
    with open(path, 'r' ,encoding="utf-8") as file:
      temp = file.read()
      temp = temp.split()
    return temp

def Get_textLines(path):
    with open(path, 'r' ,encoding="utf-8") as file:
      temp = file.readlines()
    return temp

def removeOldFile(path):
    if os.path.isfile(path):
        os.remove(path)
        print(path + "已刪除")
    else:
       print("找不到" + path)

def makedirs(path):
    if os.path.isdir(path):
        print(path+'資料夾已經存在')
    else:
      os.makedirs(path)
      print(path+'資料夾建立成功')

def writeFile(path,context):
    with open(path,"a",encoding="utf-8") as file:
        file.write(str(context))
    print(path + " 已寫入")

def csvToText(csv,path):
    for i in range (len(csv)):
      res = csv[i].split(',')
      #號碼
      number = res[0][2:6]
      #股票名稱
      a='"'
      name = re.sub(a, '', str(res[1]))
      #上市還是上櫃
      listedOrOtc = re.sub(a, '', str(res[2]))
      if i!=0 and i<len(csv)-1:
        writeFile(path, number+' '+name + ' ' + listedOrOtc + '\n')
      #最後不換行
      if i!=0 and i==len(csv)-1:
        writeFile(path, number+' '+name + ' ' + listedOrOtc)
    print(path + '檔案建立成功')

def Get_year():
   currentDateTime = datetime.datetime.now()
   year = currentDateTime.date().strftime("%Y")
   return year

def isNotHoliday(Date):
  setDate = todayYear + '-' + Date[0:2] + '-' + Date[2:]
  temp = pd.Timestamp(setDate)
  DayName = temp.day_name()
  print("今天是"+DayName)
  if DayName=='Saturday' or DayName=='Sunday':
    print('是假日')
    return False
  else:
    print('不是假日')
    return True

def get_twse_months():
    YearMonthList = []
    datetime_now = datetime.datetime.now()
    #一個月前開始
    datetime_month_ago = datetime_now - relativedelta(months = 1)
    for _ in range(3):
        # 減去一個月
        datetime_month_ago = datetime_month_ago - relativedelta(months = 1)
        #轉西元年分
        ROC_year = int(datetime_month_ago.year) - 1911
        month = int(datetime_month_ago.month)
        #放入
        YearMonthList.append(str(ROC_year) + '_' + str(month))      
    return YearMonthList
   

todayYear = Get_year()
headers_save = Get_text('data_web/headers.txt')
headers = {'user-agent': headers_save }
Class_time = Get_text_split('data_web/時間Class.txt')
Class_media = Get_text_split('data_web/媒體Class.txt')
Class_title = Get_text_split('data_web/標題Class.txt')
Class_href= Get_text_split('data_web/連結Class.txt',)
get_dayURL = Get_text('data_web/要得網址.txt')
get_InvestmentTrust_URL1 = Get_text('data_web/投信第一日上市.txt')
get_InvestmentTrust_URL2 = Get_text('data_web/投信第一日上櫃.txt')
get_historicalHigh_URL = Get_text('data_web/歷史新高.txt')
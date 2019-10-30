from calendar import monthrange 
from datetime import date

from flask_login import current_user

from ims.service.clientWorkServ import getClientWorkMonthList
from ims.service.clientWorkServ import getClientWork
from ims.contents.clientWorkCont import ClientWorkDay

def createCalendarList(month):
    """稼働情報カレンダー一覧を表示するためのListデータを作成する
    業務ロジックです

    :param month=選択された月

    """
    year = date.today().year
    if month == 0:
        month = date.today().month
    calendaDetails = list()
    # カレンダーリスト作成

    dayOfTheWeek, days = monthrange(year,month)
    if month == 1:
        _, lastMonthDays = monthrange(year-1,12)
    else:
        _, lastMonthDays = monthrange(year,month-1)
    lastMonthDays+=1

    dayOfLastMonth = list(range(lastMonthDays-dayOfTheWeek, lastMonthDays))
    dayOfThisMonth = list(range(1, days+1))
    dayOfNextMonth = list(range(1,43 - len(dayOfThisMonth) - len(dayOfLastMonth)))

    testlist = getClientWorkMonthList(current_user.user_id, year, month)

    # 先月日付取得
    for day in dayOfLastMonth:
        calendaDetails.append(ClientWorkDay(day,True))
    # 今月日付取得
    for day in dayOfThisMonth:
        #当日稼働時間を取得
        workTime = getClientWork(current_user.user_id, year, month, day)
        if workTime:
            workTime = '稼働時間 ' + workTime
            calendaDetails.append(ClientWorkDay(day,False,workTime))
        else:
            calendaDetails.append(ClientWorkDay(day,False,''))
    # 来月日付取得
    for day in dayOfNextMonth:
        calendaDetails.append(ClientWorkDay(day,True))
    
    return calendaDetails
from calendar import monthrange 
from datetime import date

from ims.common.Constants import Category
from ims.service.clientWorkServ import getClientWorkMonthDetails
from ims.service.monthlyReportServ import getMonthlyReportMonthDetails
from ims.contents.comCont import DayDetails

def createCalendarList(userId, month, category):
    """稼働情報カレンダー一覧を表示するためのListデータを作成する
    業務ロジックです

    :param userId: 選択されたユーザID
    :param month: 選択された月
    """
    year = date.today().year
    calendaDetails = list()
    # カレンダーリスト作成

    dayOfTheWeek, lastDayOfTheMonth = monthrange(year,month)
    if month == 1:
        _, theEndOfLastMonth = monthrange(year-1,12)
    else:
        _, theEndOfLastMonth = monthrange(year,month-1)
    theEndOfLastMonth+=1

    dayOfLastMonth = list(range(theEndOfLastMonth-dayOfTheWeek-1, theEndOfLastMonth))
    dayOfNextMonth = list(range(1,43 - lastDayOfTheMonth - len(dayOfLastMonth)))

    # 先月日付取得
    for day in dayOfLastMonth:
        calendaDetails.append(DayDetails(day,True))
    # 今月日付および稼働時間取得
    startDay = date(date.today().year, month, 1).strftime('%Y/%m/%d')
    endDay = date(date.today().year, month, lastDayOfTheMonth).strftime('%Y/%m/%d')

    if category == Category.CATEGORY_CLIENT_WORK:
        dayOfThisMonth = getClientWorkMonthDetails(userId, year, month, startDay, endDay)
    else:
        dayOfThisMonth = getMonthlyReportMonthDetails(userId, year, month, startDay, endDay)

    for day in dayOfThisMonth:
        if day.rest_flg == 1:
            calendaDetails.append(DayDetails(day.day, False, '休み'))
        elif day.workTime:
            calendaDetails.append(DayDetails(day.day, False, '稼働時間 ' + day.workTime, day.rest_flg))
        else:
            calendaDetails.append(DayDetails(day.day, False, '', day.rest_flg))
    # 来月日付取得
    for day in dayOfNextMonth:
        calendaDetails.append(DayDetails(day,True))

    return calendaDetails
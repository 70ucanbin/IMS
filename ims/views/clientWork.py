import calendar, datetime
from flask import request, redirect, url_for, render_template, flash, session, Blueprint
from ims.views.com import login_required
from ims.models.clientWorkDays import ClientWorkDay

clientWork = Blueprint('clientWork', __name__)

# 稼働一覧画面処理
@clientWork.route('/client_work_list/<int:month>')
@login_required
def clinent_work_list(month):
    activeCwl = 'cwl'

    year = datetime.date.today().year
    if month == 0:
        month = datetime.date.today().month
    calendaDetails = list()
    # カレンダーリスト作成

    dayOfTheWeek, days = calendar.monthrange(year,month)
    if month == 1:
        _, lastMonthDays = calendar.monthrange(year-1,12)
    else:
        _, lastMonthDays = calendar.monthrange(year,month-1)
    lastMonthDays+=1

    dayOfLastMonth = list(range(lastMonthDays-dayOfTheWeek, lastMonthDays))
    dayOfThisMonth = list(range(1, days+1))
    dayOfNextMonth = list(range(1,43 - len(dayOfThisMonth) - len(dayOfLastMonth)))

    # 先月日付取得
    for day in dayOfLastMonth:
        calendaDetails.append(ClientWorkDay(day,True))
    # 今月日付取得
    for day in dayOfThisMonth:
        calendaDetails.append(ClientWorkDay(day,False))
    # 来月日付取得
    for day in dayOfNextMonth:
        calendaDetails.append(ClientWorkDay(day,True))
    return render_template('client_work/client-work-list.html', month=month, calendaDetails=calendaDetails, activeCwl=activeCwl)


# 稼働詳細画面処理
@clientWork.route('/client_work_details/<int:month>/<int:day>')
@login_required
def clinent_work_details(month,day):
    activeCwl = 'cwl'

    try:
        datetime.date(datetime.date.today().year, month, day)
    except ValueError:
        return redirect(url_for('clientWork.clinent_work_list', month=0))

    return render_template('client_work/client-work-details.html', activeCwl=activeCwl)


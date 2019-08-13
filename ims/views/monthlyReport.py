import calendar, datetime
from flask import request, redirect, url_for, render_template, flash, session, Blueprint
from ims.views.com import login_required
from ims.models.clientWorkDays import ClientWorkDay

monthlyReport = Blueprint('monthlyReport', __name__)

# 稼働一覧画面処理
@monthlyReport.route('/monthly_report_list/<int:month>')
@login_required
def monthly_report_list(month):
    activeMr = 'mr'

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
    return render_template('monthly_report/monthly-report-list.html', month=month, calendaDetails=calendaDetails, activeMr=activeMr)


# 稼働詳細画面処理
@monthlyReport.route('/monthly_report_details/<int:month>/<int:day>')
@login_required
def monthly_report_details(month,day):
    activeMr = 'mr'

    try:
        datetime.date(datetime.date.today().year, month, day)
    except ValueError:
        return redirect(url_for('monthlyReport.monthly_report_list', month=0))

    return render_template('monthly_report/monthly-report-details.html', activeMr=activeMr)


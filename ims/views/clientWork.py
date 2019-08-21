import calendar, datetime
from flask import request, redirect, url_for, render_template, flash, session, Blueprint
from ims import db
from ims.views.com import login_required
from ims.models.clientWorkDays import ClientWorkDay
from ims.models.traClientWork import TraClientWork

clientWork = Blueprint('clientWork', __name__)

# 稼働一覧画面処理
@clientWork.route('/list/<int:month>')
@login_required
def clinent_work_list(month):
    session['activeSub'] = 'clientWork'
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
        traClientwork=TraClientWork.query.filter_by(employee_id='k4111',work_year = datetime.date.today().year, work_month = month, work_day = day).first()
        if traClientwork:
            calendaDetails.append(ClientWorkDay(day,False,'入力済'))
        else:
            calendaDetails.append(ClientWorkDay(day,False,''))
    # 来月日付取得
    for day in dayOfNextMonth:
        calendaDetails.append(ClientWorkDay(day,True))
    return render_template('client_work/client-work-list.html', month=month, calendaDetails=calendaDetails)


# 稼働詳細画面処理
@clientWork.route('/details/<int:month>/<int:day>')
@login_required
def clinent_work_details(month,day):
    try:
        datetime.date(datetime.date.today().year, month, day)
    except ValueError:
        return redirect(url_for('clientWork.clinent_work_list', month=0))

    return render_template('client_work/client-work-details.html', month=month, day=day)


# 稼働詳細画面確定処理
@clientWork.route('/details/<int:month>/<int:day>/save', methods=['POST'])
@login_required
def clinent_work_save(month, day):
    traClientwork=TraClientWork.query.filter_by(employee_id='k4111',work_year = datetime.date.today().year, work_month = month, work_day = day).first()

    try:
        traClientwork = TraClientWork(
            employee_id = 'k4111',
            work_year = datetime.date.today().year,
            work_month = month,
            work_day = day,
            order_cd = request.form['order_cd'],
            task_cd = request.form['task_cd'],
            sub_order_cd = request.form['sub_order_cd'],
            hours_of_work = request.form['hours_of_work'],
            minutes_of_work = request.form['minutes_of_work'],
            note = 'teststestsetestsetsetstes'
        )

        if traClientwork:
            db.session.merge(traClientwork)
        else:
            db.session.add(traClientwork)
        db.session.commit()
        return redirect(url_for('clientWork.clinent_work_list', month=0))
    except:
        pass


    # return render_template('client_work/client-work-details.html', activeCwl=activeCwl, workDetailsForm=workDetailsForm)

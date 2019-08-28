import calendar, datetime
from flask import request, redirect, url_for, render_template, flash, session, Blueprint, jsonify
from ims import db
from ims.views.com import login_required
from ims.mappers.models.clientWorkDays import ClientWorkDay
from ims.mappers.models.traClientWork import TraClientWork
from ims.service.clientWorkServ import getClientWork, getClientWorkList

clientWork = Blueprint('clientWork', __name__)

# 稼働カレンダー一覧画面処理
@clientWork.route('/calendar/<int:month>')
@login_required
def clinent_work_calendar(month):
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
        traClientwork=getClientWork('k4111',year, month, day)
        if traClientwork:
            calendaDetails.append(ClientWorkDay(day,False,traClientwork))
        else:
            calendaDetails.append(ClientWorkDay(day,False,''))
    # 来月日付取得
    for day in dayOfNextMonth:
        calendaDetails.append(ClientWorkDay(day,True))
    return render_template('client_work/client-work-calendar.html', month=month, calendaDetails=calendaDetails)

# 稼働情報一覧
@clientWork.route('/list/<int:month>/<int:day>', methods = ['GET','POST'])
@login_required
def clinent_work_list(month, day):
    if request.method == 'GET':

        return render_template('client_work/client-work-list.html', month=month, day=day)

    elif request.method == 'POST':
        employeeId = 'k4111'
        year = datetime.date.today().year
        month = month
        day = day

        dto = getClientWorkList(employeeId,year,month,day)
        dataset = []
        if dto:
            for d in dto:
                data = {}
                data["clientWorkId"]=d.clientWorkId
                data["workTime"]=d.workTime
                data["orderCd"]=d.orderCd
                data["taskCd"]=d.taskCd
                data["subOrderCd"]=d.subOrderCd
                dataset.append(data)

        # dataset =[{
        # "workTime": "1",
        # "orderCd": "2019-08-22",
        # "taskCd": "System Architect",
        # "subOrderCd": "$3,120"},
        # {
        # "workTime": "1",
        # "orderCd": "2019-08-22",
        # "taskCd": "System Architect",
        # "subOrderCd": "$3,120"}]
        return jsonify(dataset)
    else:
        pass

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
            # hours_of_work = request.form['hours_of_work'],
            # minutes_of_work = request.form['minutes_of_work'],
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

from datetime import date, datetime
from flask import request, redirect, url_for, render_template, Blueprint
from ims.views.com import login_required
from ims.contents.clientWorkCont import ClientWorkCalendar, ClientWorkList, ClientWorkDetails
from ims.service.clientWorkServ import getClientWork, getClientWorkList, getClientWorkDetails, insertUpdateClientWork
from ims.service.comServ import getComItemList
from ims.common.ComboBoxUtil import getNumberList, getComItem
from ims.common.BusinessLogicUtil import createCalendarList
from ims.form.cilentWorkForm import ClientWorkForm

clientWork = Blueprint('clientWork', __name__)

# 稼働カレンダー一覧画面処理
@clientWork.route('/calendar/<int:month>')
@login_required
def clinent_work_calendar(month):

    if month ==0:
        month = date.today().month

    calendaDetails = createCalendarList(month)

    monthList = getNumberList(1,13,1)

    cont = ClientWorkCalendar(month,monthList,calendaDetails)

    return render_template('client_work/client-work-calendar.html', cont=cont)

# 稼働情報一覧
@clientWork.route('/list/<int:month>/<int:day>')
@login_required
def clinent_work_list(month, day):

    employeeId = 'k4111'
    year = date.today().year

    dto = getClientWorkList(employeeId,year,month,day)

    cont = ClientWorkList(month,day,dto)

    return render_template('client_work/client-work-list.html', cont=cont)

# 稼働詳細画面処理
@clientWork.route('/details/<int:month>/<int:day>/<int:clientWorkId>', methods=['GET'])
@login_required
def clinent_work_details(month, day, clientWorkId):
    try:
        date(date.today().year, month, day)
    except ValueError:
        return redirect(url_for('clientWork.clinent_work_list', month=0))

    orderList = getComItem(getComItemList('1'))

    taskList = getComItem(getComItemList('3'))

    subOrderList = getComItem(getComItemList('2'))

    hoursList = getNumberList(0,24,1)

    minutesList = getNumberList(0,60,5)

    if clientWorkId:
        dto = getClientWorkDetails(clientWorkId)
    else:
        dto = None

    cont = ClientWorkDetails(month, day, orderList, taskList, 
        subOrderList, hoursList, minutesList, dto)

    return render_template('client_work/client-work-details-bk.html', cont=cont)

    # return render_template('client_work/client-work-details.html', cont=cont)


# 稼働詳細画面確定処理
@clientWork.route('/details/<int:month>/<int:day>', methods=['POST'])
@login_required
def clinent_work_save(month, day):

    form = request.form.to_dict()
    form['employeeId'] = 'k4111'
    form['year'] = date.today().year
    form['month'] = month
    form['day'] = day
    workTime = form['workHours']+':'+form['workMinutes']
    form['workTime'] = datetime.strptime(workTime, '%H:%M')

    if 'clientWorkId' in form:
        isUpdate = True
    else:
        isUpdate = False
    insertUpdateClientWork(form, isUpdate)

    return redirect(url_for('clientWork.clinent_work_list', month=month, day=day))


# 稼働詳細画面削除処理
@clientWork.route('/details/delete', methods=['POST'])
@login_required
def clinent_work_delete():
    
from datetime import date, datetime

from flask import flash, request, redirect, url_for, render_template, Blueprint, session
from flask_login import login_required, current_user

from config import Messages

from ims.contents.clientWorkCont import ClientWorkCalendar as calendarCont
from ims.contents.clientWorkCont import ClientWorkList as listCont
from ims.contents.clientWorkCont import ClientWorkDetails as detailCont
from ims.service.clientWorkServ import getClientWorkList, getClientWorkDetails, insertUpdateClientWork, deleteClientWork
from ims.service.comServ import getComItemList, getComUser
from ims.common.ComboBoxUtil import getNumberList, getComItem, getUserList
from ims.common.BusinessLogicUtil import createCalendarList
from ims.form.cilentWorkForm import ClientWorkForm

clientWork = Blueprint('clientWork', __name__)


@clientWork.route('/calendar/')
@login_required
def clinent_work_calendar():
    """稼働カレンダーの一覧表示  Getのrequestを受付
    ナビバーからのrequsetはディフォルトで当月を表示します。
    当処理はhtmlテンプレート及び画面用コンテンツを返します。

    :param month: 該当月のデータ取得用「月」
    :param u:管理者の場合、選択されたユーザのID
    """
    month = request.args.get('month', default = date.today().month, type = int)
    userId = request.args.get('u', type = str)
    if not userId:
        userId = session.get('cw_pick_user')
        if userId == 'undefined':
            userId = current_user.user_id

    if current_user.is_manager:
        pick_user = getComUser(userId)
        if not pick_user or pick_user.group_id != current_user.group_id:
            return redirect(url_for('clientWork.clinent_work_calendar'))
        cont = calendarCont(month)
        cont.is_manager = True
        cont.userId = pick_user.user_id
        cont.userName = pick_user.user_name
        cont.userList = getUserList(current_user.group_id)
    else:
        cont = calendarCont(month)

    cont.calendaDetails = createCalendarList(userId, month)
    cont.monthList = getNumberList(1,13,1)
    session['cw_pick_user'] = userId
    return render_template('client_work/client-work-calendar.html', cont=cont)


@clientWork.route('/list/<int:month>/<int:day>')
@login_required
def clinent_work_list(month, day):
    """稼働情報の一覧表示  Getのrequestを受付
    稼働カレンダー一覧で選択された条件のデータを取得します。
    当処理はhtmlテンプレート及び画面用コンテンツを返します。

    :param month: 選択された「月」
    :param day:選択された「日」
    """
    year = date.today().year
    userId = session.get('cw_pick_user')
    dto = getClientWorkList(userId,year,month,day)

    cont = listCont(month,day,dto)

    return render_template('client_work/client-work-list.html', cont=cont)


@clientWork.route('/details/<int:month>/<int:day>/create')
@login_required
def clinent_work_create(month, day):
    """稼働作成処理

    一覧画面から「新規作成」を押下後、GETのrequestを受付します。
    htmlテンプレート及び画面用コンテンツを返します。

    :param month: 追加対象データの月
    :param day: 追加対象データの日
    """
    try:
        date(date.today().year, month, day)
    except ValueError:
        return redirect(url_for('clientWork.clinent_work_list', month=0))

    cont = detailCont(month, day, ClientWorkForm())
    cont.is_self = True
    orderList = getComItem(getComItemList('1'))
    taskList = getComItem(getComItemList('3'))
    subOrderList = getComItem(getComItemList('2'))
    hoursList = getNumberList(0,24,1)
    minutesList = getNumberList(0,60,5)

    cont.form.orderCd.choices = [(i.key, i.value) for i in orderList]
    cont.form.taskCd.choices = [(i.key, i.value) for i in taskList]
    cont.form.subOrderCd.choices = [(i.key, i.value) for i in subOrderList]
    cont.form.workHours.choices = [(i.key, i.value) for i in hoursList]
    cont.form.workMinutes.choices = [(i.key, i.value) for i in minutesList]

    return render_template('client_work/client-work-details.html', cont=cont)


@clientWork.route('/details/<int:clientWorkId>/edit')
@login_required
def clinent_work_edit(clientWorkId):
    """稼働修正処理

    一覧画面から「稼働時間」を押下後、GETのrequestを受付します。
    htmlテンプレート及び画面用コンテンツを返します。

    :param clientWorkId: 対象データのID
    """
    dto = getClientWorkDetails(clientWorkId)
    if not dto:
        flash(Messages.WARNING_NOT_FOUND_ALREADY_UPDATED_DELETED, 
            "list-group-item list-group-item-warning")
        return redirect(url_for('clientWork.clinent_work_list', month=0))

    orderList = getComItem(getComItemList('1'))
    taskList = getComItem(getComItemList('3'))
    subOrderList = getComItem(getComItemList('2'))
    hoursList = getNumberList(0,24,1)
    minutesList = getNumberList(0,60,5)

    cont = detailCont(dto.workMonth, dto.workDay, ClientWorkForm())
    if dto.userId == current_user.user_id:
        cont.is_self = True

    cont.form.clientWorkId.data = dto.clientWorkId
    cont.form.orderCd.choices = [(i.key, i.value) for i in orderList]
    cont.form.orderCd.data = dto.orderCd
    cont.form.taskCd.choices = [(i.key, i.value) for i in taskList]
    cont.form.taskCd.data = dto.taskCd
    cont.form.subOrderCd.choices = [(i.key, i.value) for i in subOrderList]
    cont.form.subOrderCd.data = dto.subOrderCd
    cont.form.workHours.choices = [(i.key, i.value) for i in hoursList]
    cont.form.workHours.data = dto.workHours
    cont.form.workMinutes.choices = [(i.key, i.value) for i in minutesList]
    cont.form.workMinutes.data = dto.workMinutes
    cont.form.note.data = dto.note

    return render_template('client_work/client-work-details.html', cont=cont)


@clientWork.route('/details/<int:month>/<int:day>/save', methods=['POST'])
@login_required
def clinent_work_save(month, day):
    """稼働詳細画面確定処理

    formのデータをDBに保存します。
    処理終了後は稼働一覧画面へ遷移します。

    :param month: 一覧画面へ戻るときに遷移前の月を渡します。
    :param day: 一覧画面へ戻るときに遷移前の月を渡します。
    """
    form = ClientWorkForm()
    orderList = getComItem(getComItemList('1'))
    taskList = getComItem(getComItemList('3'))
    subOrderList = getComItem(getComItemList('2'))
    hoursList = getNumberList(0,24,1)
    minutesList = getNumberList(0,60,5)

    form.orderCd.choices = [(i.key, i.value) for i in orderList]
    form.taskCd.choices = [(i.key, i.value) for i in taskList]
    form.subOrderCd.choices = [(i.key, i.value) for i in subOrderList]
    form.workHours.choices = [(i.key, i.value) for i in hoursList]
    form.workMinutes.choices = [(i.key, i.value) for i in minutesList]
    if form.validate_on_submit():
        # (新規・修正)判定
        dto = getClientWorkDetails(form.clientWorkId.data)
        if form.clientWorkId.data:
            isUpdate = True
            if dto and dto.userId == current_user.user_id:
                pass
            else:
                flash(Messages.WARNING_NOT_FOUND_ALREADY_UPDATED_DELETED, 
                    "list-group-item list-group-item-warning")
                return redirect(url_for('clientWork.clinent_work_list', month=month, day=day))
        else:
            isUpdate = False

        data = form.data
        data['userId'] = current_user.user_id
        data['year'] = date.today().year
        data['month'] = month
        data['day'] = day
        workTime = str(data['workHours'])+':'+str(data['workMinutes'])
        data['workTime'] = datetime.strptime(workTime, '%H:%M')
        insertUpdateClientWork(data, isUpdate)
        if isUpdate:
            flash(Messages.SUCCESS_UPDATED, "list-group-item list-group-item-success")
        else:
            flash(Messages.SUCCESS_INSERTED, "list-group-item list-group-item-success")
        return redirect(url_for('clientWork.clinent_work_list', month=month, day=day))

    for error in form.errors.values():
        flash(error[0],"list-group-item list-group-item-danger")

    cont = detailCont(month, day, form)

    return render_template('client_work/client-work-details.html', cont=cont)



@clientWork.route('/details/<int:month>/<int:day>/<int:clientWorkId>/delete')
@login_required
def clinent_work_delete(month, day, clientWorkId):
    """稼働詳細画面削除処理

    当該データを物理削除します。
    処理終了後は稼働一覧画面へ遷移します。

    :param month: 一覧画面へ戻るときに遷移前の月を渡します。
    :param day: 一覧画面へ戻るときに遷移前の日を渡します。
    :param clientWorkId: 削除対象のIDです。
    """
    dto = getClientWorkDetails(clientWorkId)
    if dto and dto.userId == current_user.user_id:
        pass
    else:
        flash(Messages.WARNING_NOT_FOUND_ALREADY_UPDATED_DELETED, 
            "list-group-item list-group-item-warning")
        return redirect(url_for('clientWork.clinent_work_list', month=month, day=day))

    deleteClientWork(clientWorkId)
    flash(Messages.SUCCESS_DELETED, "list-group-item list-group-item-success")
    return redirect(url_for('clientWork.clinent_work_list', month=month, day=day))
from datetime import date, datetime

from flask import Blueprint, flash, jsonify, request, redirect, render_template, session, url_for
from flask_login import login_required, current_user

from ims.common.BusinessLogicUtil import createCalendarList
from ims.common.Constants import Category
from ims.common.ComboBoxUtil import getNumberList, getUserList, getOrderComBoList
from ims.common.Messages import Messages
from ims.contents.clientWorkCont import ClientWorkCalendar as calendarCont
from ims.contents.clientWorkCont import ClientWorkList as listCont
from ims.contents.clientWorkCont import ClientWorkDetails as detailCont
from ims.form.cilentWorkForm import ClientWorkForm
from ims.service.clientWorkServ import getClientWorkList as getDtoList
from ims.service.clientWorkServ import getClientWorkDetails as getDto
from ims.service.clientWorkServ import insertUpdateClientWork as insertUpdateDto
from ims.service.clientWorkServ import deleteClientWork as deleteDto
from ims.service.clientWorkServ import tookDayOff
from ims.service.comServ import getComUser
from ims.service.orderDataServ import getOrderList
from ims.service.orderDataServ import getSubOrderList

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
        if userId == 'undefined' or userId == None :
            userId = current_user.user_id

    if current_user.role == 2:
        pick_user = getComUser(userId)
        if not pick_user or pick_user.group_id != current_user.group_id:
            return redirect(url_for('clientWork.clinent_work_calendar'))
        cont = calendarCont(month)
        cont.userId = pick_user.user_id
        cont.userName = pick_user.user_name
        cont.userList = getUserList(current_user.group_id)
    else:
        cont = calendarCont(month)

    cont.calendaDetails = createCalendarList(userId, month, Category.CATEGORY_CLIENT_WORK)
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
    try:
        date(date.today().year, month, day)
    except ValueError:
        return redirect(url_for('clientWork.clinent_work_calendar'))
    year = date.today().year
    userId = session.get('cw_pick_user')
    data = getDtoList(userId,year,month,day)

    cont = listCont(month,day,data)
    if userId == current_user.user_id:
        cont.is_self = True
    return render_template('client_work/client-work-list.html', cont=cont)


@clientWork.route('/list/<int:month>/<int:day>/holiday/')
@login_required
def clinent_work_holiday(month, day):
    """稼働休み処理

    選択された日を休みとして登録します。
    既にデータが登録されている場合は、登録されたデータを削除します。
    処理終了後は月報カレンダー画面へ遷移します。

    :param month: 休み対象の登録月
    :param day: 休み対象の登録日
    """
    try:
        date(date.today().year, month, day)
    except ValueError:
        return redirect(url_for('clientWork.clinent_work_calendar', month=month))
    tookDayOff(date.today().year, month, day)
    flash(Messages.SUCCESS_UPDATED, Messages.SUCCESS_CSS)
    return redirect(url_for('clientWork.clinent_work_calendar', month=month))


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
        return redirect(url_for('clientWork.clinent_work_calendar'))

    cont = detailCont(month, day, ClientWorkForm())
    cont.is_self = True

    orderList = getOrderList(current_user.group_id)
    comboList = getOrderComBoList(orderList, True)

    hoursList = getNumberList(0,24,1)
    minutesList = getNumberList(0,60,5)

    cont.form.orderCd.choices = [(i.key, i.value) for i in comboList]
    cont.form.workHours.choices = [(i.key, i.value) for i in hoursList]
    cont.form.workMinutes.choices = [(i.key, i.value) for i in minutesList]

    return render_template('client_work/client-work-details.html', cont=cont)


@clientWork.route('/api/<orderCd>/')
@login_required
def clinent_work_api(orderCd):

    try:
        models = getSubOrderList(current_user.group_id, orderCd)
        dataset = []
        for model in models:
            data = {}
            data["subOrderCd"] = model.subOrderCd
            data["subOrderValue"] = model.subOrderValue
            dataset.append(data)
    except:
        pass
    return jsonify(dataset)


@clientWork.route('/details/<int:clientWorkId>/edit')
@login_required
def clinent_work_edit(clientWorkId):
    """稼働修正処理

    一覧画面から「稼働時間」を押下後、GETのrequestを受付します。
    htmlテンプレート及び画面用コンテンツを返します。

    :param clientWorkId: 対象データのID
    """
    dto = getDto(clientWorkId)
    if not dto:
        flash(Messages.WARNING_NOT_FOUND_ALREADY_UPDATED_DELETED, 
            Messages.WARNING_CSS)
        return redirect(url_for('clientWork.clinent_work_list', month=0))

    cont = detailCont(dto.workMonth, dto.workDay, ClientWorkForm())
    if dto.userId == current_user.user_id:
        cont.is_self = True
    orderList = getOrderComBoList(getOrderList(current_user.group_id), True)
    if dto.orderCd:
        subOrderList = getSubOrderList(current_user.group_id, dto.orderCd)
        if subOrderList:
            cont.form.subOrderCd.choices = [(i.subOrderCd, i.subOrderValue) for i in subOrderList]

    hoursList = getNumberList(0,24,1)
    minutesList = getNumberList(0,60,5)
    cont.form.clientWorkId.data = dto.clientWorkId
    cont.form.orderCd.choices = [(i.key, i.value) for i in orderList]
    cont.form.orderCd.data = dto.orderCd
    cont.form.taskCd.data = dto.taskCd
    cont.form.workHours.choices = [(i.key, i.value) for i in hoursList]
    cont.form.workHours.data = dto.workHours
    cont.form.workMinutes.choices = [(i.key, i.value) for i in minutesList]
    cont.form.workMinutes.data = dto.workMinutes
    cont.form.note.data = dto.note

    return render_template('client_work/client-work-details.html', cont=cont)


@clientWork.route('/details/<int:month>/<int:day>/save', methods=['POST'])
@login_required
def clinent_work_save(month, day):
    """稼働詳細画面登録処理

    formのデータをDBに保存します。
    処理終了後は稼働一覧画面へ遷移します。

    :param month: 一覧画面へ戻るときに遷移前の月を渡します。
    :param day: 一覧画面へ戻るときに遷移前の月を渡します。
    """
    form = ClientWorkForm()
    orderList = getOrderComBoList(getOrderList(current_user.group_id), True)
    if form.orderCd.data:
        subOrderList = getSubOrderList(current_user.group_id, form.orderCd.data)
        if subOrderList:
            form.subOrderCd.choices = [(i.subOrderCd, i.subOrderValue) for i in subOrderList]
    hoursList = getNumberList(0,24,1)
    minutesList = getNumberList(0,60,5)

    form.orderCd.choices = [(i.key, i.value) for i in orderList]
    form.workHours.choices = [(i.key, i.value) for i in hoursList]
    form.workMinutes.choices = [(i.key, i.value) for i in minutesList]
    if form.validate_on_submit():
        # (新規・修正)判定
        dto = getDto(form.clientWorkId.data)
        if form.clientWorkId.data:
            isUpdate = True
            if dto and dto.userId == current_user.user_id:
                pass
            else:
                flash(Messages.WARNING_NOT_FOUND_ALREADY_UPDATED_DELETED, 
                    Messages.WARNING_CSS)
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
        insertUpdateDto(data, isUpdate)
        if isUpdate:
            flash(Messages.SUCCESS_UPDATED, Messages.SUCCESS_CSS)
        else:
            flash(Messages.SUCCESS_INSERTED, Messages.SUCCESS_CSS)
        return redirect(url_for('clientWork.clinent_work_list', month=month, day=day))

    for error in form.errors.values():
        flash(error[0],Messages.DANGER_CSS)

    cont = detailCont(month, day, form)
    cont.is_self = True

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
    dto = getDto(clientWorkId)
    if dto and dto.userId == current_user.user_id:
        pass
    else:
        flash(Messages.WARNING_NOT_FOUND_ALREADY_UPDATED_DELETED, 
            Messages.WARNING_CSS)
        return redirect(url_for('clientWork.clinent_work_list', month=month, day=day))

    deleteDto(clientWorkId)
    flash(Messages.SUCCESS_DELETED, Messages.SUCCESS_CSS)
    return redirect(url_for('clientWork.clinent_work_list', month=month, day=day))
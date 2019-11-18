import urllib.parse

from datetime import date, datetime

from flask import Blueprint, flash, make_response, redirect, render_template, request, url_for, session
from flask_login import login_required, current_user

from ims.common.AppPath import PathConfig as path
from ims.common.BusinessLogicUtil import createCalendarList
from ims.common.Constants import Category
from ims.common.ComboBoxUtil import getNumberList, getComItem, getUserList
from ims.common.ExcelLogicUtil import monthly_report_excel as getFile
from ims.common.Messages import Messages
from ims.contents.monthlyReportCont import MonthlyReportCalendar as calendarCont
from ims.contents.monthlyReportCont import MonthlyReportDetails as detailCont
from ims.form.monthlyReportForm import MonthlyReportForm
from ims.service.comServ import getComUser
from ims.service.monthlyReportServ import insertUpdateMonthlyReport as insertUpdateDto
from ims.service.monthlyReportServ import getMonthlyReportList as getDtoList
from ims.service.monthlyReportServ import getMonthlyReportDetails as getDto
from ims.service.monthlyReportServ import deleteMonthlyReport as deleteDto
from ims.service.monthlyReportServ import tookDayOff

monthlyReport = Blueprint('monthlyReport', __name__)


@monthlyReport.route('/calendar/')
@login_required
def monthly_report_calendar():
    """月報カレンダーの一覧表示  Getのrequestを受付
    ナビバーからのrequsetはディフォルトで当月を表示します。
    当処理はhtmlテンプレート及び画面用コンテンツを返します。

    :param month: 該当月のデータ取得用「月」
    :param u:管理者の場合、選択されたユーザのID
    """
    month = request.args.get('month', default = date.today().month, type = int)
    userId = request.args.get('u', type = str)
    if not userId:
        userId = session.get('mr_pick_user')
        if userId == 'undefined' or userId == None :
            userId = current_user.user_id

    if current_user.is_manager == 1:
        pick_user = getComUser(userId)
        if not pick_user or pick_user.group_id != current_user.group_id:
            return redirect(url_for('monthlyReport.monthly_report_calendar', month=month))
        cont = calendarCont(month)
        cont.is_manager = True
        cont.userId = pick_user.user_id
        cont.userName = pick_user.user_name
        cont.userList = getUserList(current_user.group_id)
    else:
        cont = calendarCont(month)

    cont.calendaDetails = createCalendarList(userId, month, Category.CATEGORY_MONTHLY_REPORT)
    cont.monthList = getNumberList(1,13,1)
    session['mr_pick_user'] = userId
    return render_template('monthly_report/monthly-report-calendar.html', cont=cont)

@monthlyReport.route('/calendar/<int:month>/download/')
@login_required
def monthly_report_download(month):
    """月報出力処理

    月報カレンダー画面から「詳細出力」を押下後、データを帳票に書き込み、返します。

    :param month: 出力したい「月」
    """
    year = date.today().year
    try:
        date(year, month, 1)
    except ValueError:
        return redirect(url_for('monthlyReport.monthly_report_calendar'))

    userId = session.get('mr_pick_user')

    data = {}
    data['year'] = str(year)
    data['month'] = str(month)
    data['models'] = getDtoList(userId, year, month)

    templatePath = path.MONTHLY_REPORT_EXCEL_TEMPLATE
    tmpPath = path.TMP + current_user.user_id + datetime.now().strftime('%Y%m%d%H%M%S')
    # パーセントエンコード
    fileName = urllib.parse.quote(path.MONTHLY_REPORT_EXCEL_FILE_NAME)

    # Excel処理
    fileData = getFile(templatePath, tmpPath)

    # レスポンス作成
    response = make_response()
    response.data = fileData.edit_file(userId, data)
    response.headers['Content-Disposition'] = 'attachment; filename=' + '"' + fileName + '";filename*=UTF-8\'\'' + fileName
    response.mimetype = 'application/vnd.ms-excel'

    return response

@monthlyReport.route('/details/<int:month>/<int:day>/')
@login_required
def monthly_report_details(month, day):
    """月報詳細画面処理

    カレンダー一覧画面から日を押下後、GETのrequestを受付します。
    htmlテンプレート及び画面用コンテンツを返します。

    :param month: 対象データの月
    :param day: 対象データの日
    """
    try:
        date(date.today().year, month, day)
    except ValueError:
        return redirect(url_for('monthlyReport.monthly_report_calendar'))

    userId = session.get('mr_pick_user')
    cont = detailCont(month, day)

    if userId == current_user.user_id:
        cont.is_self = True

    dto = getDto(userId, date.today().year, month, day)
    if dto and dto.rest_flg != None:
        isUpdate = True
    else:
        isUpdate = False

    cont.form = MonthlyReportForm()
    cont.is_update = isUpdate
    hoursList = getNumberList(0,24,1)
    minutesList = getNumberList(0,60,5)

    cont.form.startWorkHours.choices = [(i.key, i.value) for i in hoursList]
    cont.form.startWorkMinutes.choices = [(i.key, i.value) for i in minutesList]
    cont.form.endWorkHours.choices = [(i.key, i.value) for i in hoursList]
    cont.form.endWorkMinutes.choices = [(i.key, i.value) for i in minutesList]

    if isUpdate:
        cont.form.workDetails.data = dto.workDetails
        cont.form.startWorkHours.data = dto.startWorkHours
        cont.form.startWorkMinutes.data = dto.startWorkMinutes
        cont.form.endWorkHours.data = dto.endWorkHours
        cont.form.endWorkMinutes.data = dto.endWorkMinutes
        cont.form.normalWorkingHours.data = dto.normalWorkingHours
        cont.form.overtimeHours.data = dto.overtimeHours
        cont.form.holidayWorkHours.data = dto.holidayWorkHours
        cont.form.note.data = dto.note

    return render_template('monthly_report/monthly-report-details.html', cont=cont)
        

@monthlyReport.route('/details/<int:month>/<int:day>/save/', methods=['POST'])
@login_required
def monthly_report_save(month, day):
    """月報詳細画面登録処理

    formのデータをDBに保存します。
    処理終了後は月報カレンダー画面へ遷移します。

    :param month: 登録月
    :param day: 登録日
    """
    try:
        date(date.today().year, month, day)
    except ValueError:
        return redirect(url_for('monthlyReport.monthly_report_calendar'))

    userId = session.get('mr_pick_user')
    dto = getDto(userId, date.today().year, month, day)
    if dto:
        isUpdate = True
        if dto.userId == current_user.user_id:
            pass
        else:
            flash(Messages.WARNING_NOT_FOUND_ALREADY_UPDATED_DELETED, 
                Messages.WARNING_CSS)
            return redirect(url_for('monthlyReport.monthly_report_calendar', month=month))

    else:
        isUpdate = False

    hoursList = getNumberList(0,24,1)
    minutesList = getNumberList(0,60,5)
    form = MonthlyReportForm()
    form.startWorkHours.choices = [(i.key, i.value) for i in hoursList]
    form.startWorkMinutes.choices = [(i.key, i.value) for i in minutesList]
    form.endWorkHours.choices = [(i.key, i.value) for i in hoursList]
    form.endWorkMinutes.choices = [(i.key, i.value) for i in minutesList]
    if form.validate_on_submit():
        data = form.data
        data['userId'] = current_user.user_id
        data['year'] = date.today().year
        data['month'] = month
        data['day'] = day
        startWorkTime = str(data['startWorkHours'])+':'+str(data['startWorkMinutes'])
        endWorkTime = str(data['endWorkHours'])+':'+str(data['endWorkMinutes'])
        data['startWorkTime'] = datetime.strptime(startWorkTime, '%H:%M')
        data['endWorkTime'] = datetime.strptime(endWorkTime, '%H:%M')

        insertUpdateDto(data, isUpdate)

        return redirect(url_for('monthlyReport.monthly_report_calendar', month=month))

    for error in form.errors.values():
        flash(error[0], Messages.DANGER_CSS)

    cont = detailCont(month, day)
    cont.form = form

    return render_template('monthly_report/monthly-report-details.html', cont=cont)

@monthlyReport.route('/details/<int:month>/<int:day>/holiday/')
@login_required
def monthly_report_holiday(month, day):
    """月報詳細休み処理

    選択された日を休みとして登録します。
    既にデータが登録されている場合は、登録されたデータを削除します。
    処理終了後は月報カレンダー画面へ遷移します。

    :param month: 休み対象の登録月
    :param day: 休み対象の登録日
    """
    try:
        date(date.today().year, month, day)
    except ValueError:
        return redirect(url_for('monthlyReport.monthly_report_calendar'))
    tookDayOff(date.today().year, month, day)
    flash(Messages.SUCCESS_UPDATED, Messages.SUCCESS_CSS)
    return redirect(url_for('monthlyReport.monthly_report_calendar', month=month))


@monthlyReport.route('/details/<int:month>/<int:day>/delete/')
@login_required
def monthly_report_delete(month, day):
    """月報詳細画面削除処理

    当該データを物理削除します。
    処理終了後は月報カレンダー画面へ遷移します。

    :param month: 削除対象の登録月
    :param day: 削除対象の登録日
    """
    try:
        date(date.today().year, month, day)
    except ValueError:
        return redirect(url_for('monthlyReport.monthly_report_calendar'))

    userId = session.get('mr_pick_user')
    dto = getDto(userId, date.today().year, month, day)
    if dto and dto.userId == current_user.user_id:
        pass
    else:
        flash(Messages.WARNING_NOT_FOUND_ALREADY_UPDATED_DELETED, 
            Messages.WARNING_CSS)
        return redirect(url_for('monthlyReport.monthly_report_calendar', month=month))

    deleteDto(date.today().year, month, day)
    flash(Messages.SUCCESS_DELETED, Messages.SUCCESS_CSS)
    return redirect(url_for('monthlyReport.monthly_report_calendar', month=month))
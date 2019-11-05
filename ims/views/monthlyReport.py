from datetime import date, datetime

from flask import flash, request, redirect, url_for, render_template, Blueprint, session
from flask_login import login_required, current_user

from config import Messages

from ims.contents.monthlyReportCont import MonthlyReportCalendar as calendarCont
from ims.contents.monthlyReportCont import MonthlyReportDetails as detailCont
from ims.service.clientWorkServ import getClientWorkList, getClientWorkDetails, insertUpdateClientWork, deleteClientWork
from ims.service.comServ import getComItemList, getComUser
from ims.common.ComboBoxUtil import getNumberList, getComItem, getUserList
from ims.common.BusinessLogicUtil import createCalendarList
from ims.form.cilentWorkForm import ClientWorkForm


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
        if userId == None:
            userId = current_user.user_id

    if current_user.is_manager:
        pick_user = getComUser(userId)
        if not pick_user or pick_user.group_id != current_user.group_id:
            return redirect(url_for('monthlyReport.monthly_report_calendar'))
        cont = calendarCont(month)
        cont.is_manager = True
        cont.userId = pick_user.user_id
        cont.userName = pick_user.user_name
        cont.userList = getUserList(current_user.group_id)
    else:
        cont = calendarCont(month)

    cont.calendaDetails = createCalendarList(userId, month)
    cont.monthList = getNumberList(1,13,1)
    session['mr_pick_user'] = userId
    return render_template('monthly_report/monthly-report-calendar.html', cont=cont)



# # 月報詳細画面処理
# @monthlyReport.route('/details/<int:month>/<int:day>')
# @login_required
# def monthly_report_details(month,day):
#     try:
#         datetime.date(datetime.date.today().year, month, day)
#     except ValueError:
#         return redirect(url_for('monthlyReport.monthly_report_list', month=0))

#     cont = MonthlyReportDetailsCont(month,day)

#     return render_template('monthly_report/monthly-report-details.html', cont=cont, activeSub='monthlyReport')
        
# # 月報詳細画面確定処理
# @monthlyReport.route('/details/<int:month>/<int:day>/save', methods=['POST'])
# @login_required
# def monthly_report_save(month, day):

#     _traMonthlyReportDto = TraMonthlyReport(
#         employee_id = 'k4111',
#         work_year = datetime.date.today().year,
#         work_month = month,
#         work_day = day,
#         work_details = request.form['work_details'],
#         start_work_hours = request.form['start_work_hours'],
#         start_work_minutes = request.form['start_work_minutes'],
#         end_work_hours = request.form['end_work_hours'],
#         end_work_minutes = request.form['end_work_minutes'],
#         normal_working_hours = request.form['normal_working_hours'],
#         overtime_hours = request.form['overtime_hours'],
#         holiday_work_hours = request.form['holiday_work_hours'],
#         note = request.form['note']
#     )
#     _traMonthlyReport = TraMonthlyReport.query.filter_by(employee_id='k4111', \
#         work_year = datetime.date.today().year, work_month = month, work_day = day).first()
#     if TraMonthlyReport:
#         db.session.merge(_traMonthlyReportDto)
#     else:
#         db.session.add(_traMonthlyReportDto)
#     db.session.commit()
#     return redirect(url_for('monthlyReport.monthly_report_list', month=0))

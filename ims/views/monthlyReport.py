import calendar, datetime
from flask import request, redirect, url_for, render_template, flash, session, Blueprint
from ims import db
from ims.views.com import login_required
from ims.models.traMonthlyReport import TraMonthlyReport
from ims.form.monthlyReportForm import MonthlyReportListForm, MonthlyReportDetailsForm


monthlyReport = Blueprint('monthlyReport', __name__)

# 月報一覧画面処理
@monthlyReport.route('/list/<int:month>')
@login_required
def monthly_report_list(month):

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
        calendaDetails.append(MonthlyReportListForm(day,True))
    # 今月日付取得
    for day in dayOfThisMonth:
        monthlyReport=TraMonthlyReport.query.filter_by(employee_id='k4111', \
            work_year = datetime.date.today().year, work_month = month, work_day = day).first()
        if monthlyReport:
            monthlyReportListForm = MonthlyReportListForm(day,False,False, \
                monthlyReport.start_work_hours, monthlyReport.start_work_minutes, \
                monthlyReport.end_work_hours, monthlyReport.end_work_minutes)
            calendaDetails.append(monthlyReportListForm)
        else:
            calendaDetails.append(MonthlyReportListForm(day,False))
    # 来月日付取得
    for day in dayOfNextMonth:
        calendaDetails.append(MonthlyReportListForm(day,True))
    return render_template('monthly_report/monthly-report-list.html', month=month, \
        calendaDetails=calendaDetails, activeSub='monthlyReport')


# 月報詳細画面処理
@monthlyReport.route('/details/<int:month>/<int:day>')
@login_required
def monthly_report_details(month,day):
    activeMr = 'mr'

    try:
        datetime.date(datetime.date.today().year, month, day)
    except ValueError:
        return redirect(url_for('monthlyReport.monthly_report_list', month=0))

    traMonthlyReport = TraMonthlyReport.query.filter_by(employee_id='k4111', \
        work_year = datetime.date.today().year, work_month = month, work_day = day).first()

    detailsForm = MonthlyReportDetailsForm(traMonthlyReport)

    return render_template('monthly_report/monthly-report-details.html', \
        month=month, day=day, detailsForm=detailsForm, activeSub='monthlyReport')
        
# 月報詳細画面確定処理
@monthlyReport.route('/details/<int:month>/<int:day>/save', methods=['POST'])
@login_required
def monthly_report_save(month, day):

    _traMonthlyReportDto = TraMonthlyReport(
        employee_id = 'k4111',
        work_year = datetime.date.today().year,
        work_month = month,
        work_day = day,
        work_details = request.form['work_details'],
        start_work_hours = request.form['start_work_hours'],
        start_work_minutes = request.form['start_work_minutes'],
        end_work_hours = request.form['end_work_hours'],
        end_work_minutes = request.form['end_work_minutes'],
        normal_working_hours = request.form['normal_working_hours'],
        overtime_hours = request.form['overtime_hours'],
        holiday_work_hours = request.form['holiday_work_hours'],
        note = request.form['note']
    )
    _traMonthlyReport = TraMonthlyReport.query.filter_by(employee_id='k4111', \
        work_year = datetime.date.today().year, work_month = month, work_day = day).first()
    if TraMonthlyReport:
        db.session.merge(_traMonthlyReportDto)
    else:
        db.session.add(_traMonthlyReportDto)
    db.session.commit()
    return redirect(url_for('monthlyReport.monthly_report_list', month=0))

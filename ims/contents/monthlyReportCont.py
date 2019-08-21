import calendar, datetime
from ims.com.selectBox import monthList, hoursList, minutesList
from ims.models.traMonthlyReport import TraMonthlyReport

class MonthlyReportListCont:
    def __init__(self, month=None):
        self.month = month
        self.dayDetails = list()
        self.monthList = monthList(1,13,1).selectList

        # カレンダーリスト作成
        year = datetime.date.today().year
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
            self.dayDetails.append(_DayDetails(day,True))
        # 今月日付取得
        for day in dayOfThisMonth:
            monthlyReport = TraMonthlyReport.query.filter_by(employee_id='k4111', \
                work_year = datetime.date.today().year, work_month = month, work_day = day).first()
            if monthlyReport:
                monthlyReportListCont = _DayDetails(day,False,False, \
                    monthlyReport.start_work_hours, monthlyReport.start_work_minutes, \
                    monthlyReport.end_work_hours, monthlyReport.end_work_minutes)
                self.dayDetails.append(monthlyReportListCont)
            else:
                self.dayDetails.append(_DayDetails(day,False))
        # 来月日付取得
        for day in dayOfNextMonth:
            self.dayDetails.append(_DayDetails(day,True))


class _DayDetails:
    def __init__(self, day=None, disabled=True, noData=True, \
        start_work_hours=None, start_work_minutes=None, \
        end_work_hours=None, end_work_minutes=None):
        self.day = day
        self.disabled = disabled
        self.noData = noData
        self.startWorkTime = "%s : %s" % (str(start_work_hours).zfill(2), str(start_work_minutes).zfill(2))
        self.endWorkTime = "%s : %s" % (str(end_work_hours).zfill(2), str(end_work_minutes).zfill(2))


class MonthlyReportDetailsCont:
    def __init__(self, month=None, day=None):
        self.month = month
        self.day = day
        self.hoursList = hoursList(6,24,1).selectList
        self.minutesList = minutesList(0,60,5).selectList
        year = datetime.date.today().year
        self.traMonthlyReport = TraMonthlyReport.query.filter_by(employee_id='k4111', \
            work_year = year, work_month = month, work_day = day).first()
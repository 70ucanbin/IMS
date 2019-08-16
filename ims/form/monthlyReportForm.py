from ims.com.selectBox import HoursList, MinutesList
from ims.models.traMonthlyReport import TraMonthlyReport

class MonthlyReportListForm:
    def __init__(self, day=None, disabled=None, noData=True, \
        start_work_hours=None, start_work_minutes=None, \
        end_work_hours=None, end_work_minutes=None):
        self.day = day
        self.disabled = disabled
        self.noData = noData
        self.startWorkTime = "%s : %s" % (str(start_work_hours).zfill(2), str(start_work_minutes).zfill(2))
        self.endWorkTime = "%s : %s" % (str(end_work_hours).zfill(2), str(end_work_minutes).zfill(2))

class MonthlyReportDetailsForm:
    def __init__(self, TraMonthlyReport=None):
        self.traMonthlyReport = TraMonthlyReport
        self.hoursList = HoursList(6,24,1).selectList
        self.minutesList = MinutesList(0,60,5).selectList
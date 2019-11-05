
class MonthlyReportCalendar:
    def __init__(self, month=None):
        self.month = month
        self.is_manager = False
        self.userId = None
        self.userName = None
        self.userList = None
        self.monthList = None
        self.calendaDetails = None
 

class MonthlyReportDay:
    def __init__(self, day=None, disabled=None, workTime=None):
        self.day = day
        self.disabled = disabled
        self.workTime = workTime

    def __repr__(self):
        return '<workDay day:{}>'.format(self.day)


class MonthlyReportDetails:
    def __init__(self, month=None, day=None, form = None):
        self.is_self = False
        self.month = month
        self.day = day
        self.form = form

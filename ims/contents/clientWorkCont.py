
class ClientWorkCalendar:
    def __init__(self, month=None):
        self.month = month
        self.is_manager = False
        self.userId = None
        self.userName = None
        self.userList = None
        self.monthList = None
        self.calendaDetails = None
 

class ClientWorkDay:
    def __init__(self, day=None, disabled=None, workTime=None):
        self.day = day
        self.disabled = disabled
        self.workTime = workTime


class ClientWorkList:
    def __init__(self, month=None, day=None, data=None):
        self.month = month
        self.day = day
        self.dataSet = data


class ClientWorkDetails:
    def __init__(self, month=None, day=None, form = None):
        self.is_self = False
        self.month = month
        self.day = day
        self.form = form
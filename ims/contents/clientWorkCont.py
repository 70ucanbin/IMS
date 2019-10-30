
class ClientWorkCalendar:
    def __init__(self, month=None, monthList=None, data=None):
        self.month = month
        self.is_manager = False
        self.userList = None
        self.monthList = monthList
        self.calendaDetails = data
 

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
    def __init__(self, month=None, day=None,
            orderList=None, taskList=None, subOrderList=None,
            hoursList=None, minutesList=None, data=None):
        self.month = month
        self.day = day
        self.orderList = orderList
        self.taskList = taskList
        self.subOrderList = subOrderList
        self.hoursList = hoursList
        self.minutesList = minutesList
        self.formData = data
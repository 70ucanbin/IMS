
class TravelExpensesListCont:
    def __init__(self, month=None, monthList=None):
        self.month = month
        self.is_manager = False
        self.userList = None
        self.monthList = monthList


class _TravelExpensesCont:
    def __init__(self, expenseDate=None, expenseItem=None, route=True, \
        transit=None, payment=None, uploadFile=None):
        self.expenseDate = expenseDate
        self.expenseItem = expenseItem
        self.route = route
        self.transit = transit
        self.payment = payment
        if uploadFile != None:
            self.uploadFile = True
        else:
            self.uploadFile = False

class TravelExpensesDetailsCont:
    def __init__(self, month=None, data=None):
        self.month = month
        self.is_self = False
        self.form = data
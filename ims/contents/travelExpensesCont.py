import datetime
from ims.com.selectBox import hoursList, minutesList
from ims.models.traTravelExpenses import TraTravelExpenses

class TravelExpensesListCont:
    def __init__(self, month=None):
        self.dataset = list()
        year = datetime.date.today().year

        traTravelExpenses = TraTravelExpenses.query.filter_by(employee_id='k4111', \
            work_year = year, work_month = month)
        if traTravelExpenses:
            for dto in traTravelExpenses:
                data = _TravelExpensesCont(
                    dto.travel_expenses_id,
                    dto.expense_date,
                    dto.expense_item,
                    dto.route,
                    dto.payment,
                    dto.attached_file_id
                )
                self.dataset.append(data)

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
    def __init__(self, TraTravelExpenses=None):
        self.TraTravelExpenses = TraTravelExpenses
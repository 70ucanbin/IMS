from ims.com.selectBox import HoursList, MinutesList
from ims.models.traTravelExpenses import TraTravelExpenses

class TravelExpensesListForm:
    def __init__(self, expenseDate=None, expenseItem=None, route=True, \
        transit=None, payment=None, uploadFile=None):
        self.expenseDate = expenseDate
        self.expenseItem = expenseItem
        self.route = route
        self.transit = transit
        self.payment = payment
        self.uploadFile = uploadFile

class TravelExpensesDetailsForm:
    def __init__(self, TraTravelExpenses=None):
        self.TraTravelExpenses = TraTravelExpenses
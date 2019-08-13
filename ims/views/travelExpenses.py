import calendar, datetime
from flask import request, redirect, url_for, render_template, flash, session, Blueprint
from ims.views.com import login_required
from ims.models.clientWorkDays import ClientWorkDay

travelExpenses = Blueprint('travelExpenses', __name__)

@travelExpenses.route('/travel_expenses_list/<int:month>')
@login_required
def travel_expenses_list(month):
    activeTe = 'cwl'
    if month == 0:
        month = datetime.date.today().month
    else:
        pass
    return render_template('travel_expenses/travel-expenses-list.html', month=month, activeTe=activeTe)

@travelExpenses.route('/travel_expenses_details/<int:travelExpensesId>')
@login_required
def travel_expenses_details(travelExpensesId=None):
    activeTe = 'cwl'
    if travelExpensesId==None:
        print(travelExpensesId)
    else:
        print(travelExpensesId)
    return render_template('travel_expenses/travel-expenses-details.html', activeTe=activeTe)
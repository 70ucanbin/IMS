import calendar
from datetime import date, datetime
from flask import request, redirect, url_for, render_template, flash, session, Blueprint, jsonify
from ims import db
from ims.views.com import login_required
from ims.mappers.models.traTravelExpenses import TraTravelExpenses
from ims.contents.travelExpensesCont import TravelExpensesList, TravelExpensesListCont, TravelExpensesDetailsCont
from ims.common.ExcelLogicUtil import travelExpenses_excel as getFile
from ims.service.travelExpensesServ import getTravelExpenses
from ims.common.ComboBoxUtil import getNumberList


travelExpenses = Blueprint('travelExpenses', __name__)

@travelExpenses.route('/travel_expenses_list/<int:month>', methods = ['GET','POST'])
@login_required
def travel_expenses_list(month):
    if request.method == 'GET':
        if month == 0:
            month = date.today().month

        monthList = getNumberList(1,13,1)

        cont = TravelExpensesList(month, monthList)

        return render_template('travel_expenses/travel-expenses-list.html', cont=cont)
    elif request.method == 'POST':
        # dataset = TravelExpensesListCont(month).dataset
        if request:
            print(request.data)
        dataset =[{
        "travelExpensesId": "1",
        "expenseDate": "2019-08-22",
        "expenseItem": "System Architect",
        "route": "$3,120",
        "transit": "Edinburgh",
        "payment": "5421",
        "uploadFile": "5421"}]
        return jsonify(dataset)
    else:
        pass


@travelExpenses.route('/travel_expenses_list/<int:month>/download', methods = ['GET','POST'])
@login_required
def travel_expenses_download(month):
    print(__file__)
    user = 'k4111'
    year = date.today().year
    models = getTravelExpenses(user, year, month)

    file_path = 'D:\\YO\\IMS\\ims\\contents\\excelTemplate\\travelExpenses.xlsx'

    data = getFile(file_path)
    result =data.edit_file(models)
    
    return jsonify(result)















@travelExpenses.route('/travel_expenses_details/<int:month>/<int:travelExpensesId>')
@login_required
def travel_expenses_details(month, travelExpensesId):
    if travelExpensesId==None:
        print(travelExpensesId)
    else:
        _traTravelExpenses = TraTravelExpenses.query.get(travelExpensesId)

    cont = TravelExpensesDetailsCont(_traTravelExpenses)
    return render_template('travel_expenses/travel-expenses-details.html', month=month, \
        travelExpensesId=travelExpensesId, cont=cont)


@travelExpenses.route('/travel_expenses_details/<int:month>/<int:travelExpensesId>/save', methods=['POST'])
@login_required
def travel_expenses_save(month, travelExpensesId):
    _traTravelExpensesDto = TraTravelExpenses(
        employee_id = 'k4111',
        work_year = datetime.date.today().year,
        work_month =  month,
        expense_date = request.form['expense_date'],
        expense_item = request.form['expense_item'],
        route = request.form['route'],
        transit = request.form['transit'],
        payment = request.form['payment'],
        attached_file_id = 'k4111',
        note = request.form['note']
    )
    if travelExpensesId != 0:
        _traTravelExpenses = TraTravelExpenses.query.get(travelExpensesId)
        _traTravelExpensesDto.travel_expenses_id = travelExpensesId
        db.session.merge(_traTravelExpensesDto)
    else:
        db.session.add(_traTravelExpensesDto)
    db.session.commit()
    return redirect(url_for('travelExpenses.travel_expenses_list', month=0))
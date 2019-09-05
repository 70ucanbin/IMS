from datetime import date, datetime
from flask import request, redirect, url_for, render_template, flash, session, Blueprint, jsonify, make_response
from ims import db
from ims.views.com import login_required
from ims.mappers.models.traTravelExpenses import TraTravelExpenses
from ims.contents.travelExpensesCont import TravelExpensesList, TravelExpensesListCont, TravelExpensesDetailsCont
from ims.common.ExcelLogicUtil import travelExpenses_excel as getFile
from ims.service.travelExpensesServ import getTravelExpensesList
from ims.common.ComboBoxUtil import getNumberList
import json

travelExpenses = Blueprint('travelExpenses', __name__)

@travelExpenses.route('/travel_expenses_list/<int:month>', methods = ['GET'])
@login_required
def travel_expenses_list(month):
    if month == 0:
        month = date.today().month

    monthList = getNumberList(1,13,1)

    cont = TravelExpensesList(month, monthList)

    return render_template('travel_expenses/travel-expenses-list.html', cont=cont)


@travelExpenses.route('/travel_expenses_list/getData', methods = ['POST'])
@login_required
def travel_expenses_post_data():

    if request:
        print(request.json)

    user = 'k4111'
    year = date.today().year
    month = int(request.json['month'])
    models = getTravelExpensesList(user, year, month)

    dataset = []
    for model in models:
        data = {}
        data["travelExpensesId"] = model.travel_expenses_id
        data["expenseDate"] = model.expense_date
        data["expenseItem"] = model.expense_item
        data["route"] = model.route
        data["transit"] = model.transit
        data["payment"] = model.payment
        data["uploadFile"] = model.attached_file_id
        dataset.append(data)

    return jsonify(dataset)


@travelExpenses.route('/travel_expenses_list/<int:month>/download', methods = ['GET','POST'])
@login_required
def travel_expenses_download(month):
    print(__file__)
    user = 'k4111'
    year = date.today().year
    models = getTravelExpensesList(user, year, month)

    file_path = 'D:\\YO\\IMS\\ims\\contents\\excelTemplate\\travelExpenses.xlsx'
    tmp_path ='tmp\\'+ user + datetime.now().strftime('%Y%m%d%H%M%S')

    data = getFile(file_path, tmp_path)

    response = make_response()
    response.data = data.edit_file(models)
    downloadFileName = 'test' + user + '.xlsx' 
    response.headers['Content-Disposition'] = 'attachment; filename=' + downloadFileName
    response.mimetype = 'application/vnd.ms-excel'

    return response




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
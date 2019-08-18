import calendar, datetime
from flask import request, redirect, url_for, render_template, flash, session, Blueprint, jsonify
from ims import db
from ims.views.com import login_required
from ims.models.traTravelExpenses import TraTravelExpenses
from ims.form.travelExpensesForm import TravelExpensesListForm, TravelExpensesDetailsForm

travelExpenses = Blueprint('travelExpenses', __name__)

@travelExpenses.route('/travel_expenses_list/<int:month>', methods = ['GET','POST'])
@login_required
def travel_expenses_list(month):
    if request.method == 'GET':
        if month == 0:
            month = datetime.date.today().month
        else:
            pass
        return render_template('travel_expenses/travel-expenses-list.html', month=month, activeSub='travelExpenses')
    elif request.method == 'POST':
        dataset =[{
        "name": "testn",
        "position": "System Architect",
        "salary": "$3,120",
        "start_date": "Edinburgh",
        "office": "5421",
        "extn": "5421"},
        {
        "name": "testn",
        "position": "System Architect",
        "salary": "$3,120",
        "start_date": "Edinburgh",
        "office": "5421",
        "extn": "5421"},
        {
        "name": "testn",
        "position": "System Architect",
        "salary": "$3,120",
        "start_date": "Edinburgh",
        "office": "5421",
        "extn": "5421"},
        {
        "name": "testn",
        "position": "System Architect",
        "salary": "$3,120",
        "start_date": "Edinburgh",
        "office": "5421",
        "extn": "5421"},
        {
        "name": "testn",
        "position": "System Architect",
        "salary": "$3,120",
        "start_date": "Edinburgh",
        "office": "5421",
        "extn": "5421"},
        {
        "name": "testn",
        "position": "System Architect",
        "salary": "$3,120",
        "start_date": "Edinburgh",
        "office": "5421",
        "extn": "5421"},
        {
        "name": "testn",
        "position": "System Architect",
        "salary": "$3,120",
        "start_date": "Edinburgh",
        "office": "5421",
        "extn": "5421"},
        {
        "name": "testn",
        "position": "System Architect",
        "salary": "$3,120",
        "start_date": "Edinburgh",
        "office": "5421",
        "extn": "5421"},
        {
        "name": "testn",
        "position": "System Architect",
        "salary": "$3,120",
        "start_date": "Edinburgh",
        "office": "5421",
        "extn": "5421"},
        {
        "name": "testn",
        "position": "System Architect",
        "salary": "$3,120",
        "start_date": "Edinburgh",
        "office": "5421",
        "extn": "5421"},
        {
        "name": "testn",
        "position": "System Architect",
        "salary": "$3,120",
        "start_date": "Edinburgh",
        "office": "5421",
        "extn": "5421"},
        {
        "name": "testn",
        "position": "System Architect",
        "salary": "$3,120",
        "start_date": "Edinburgh",
        "office": "5421",
        "extn": "5421"},
        {
        "name": "testn",
        "position": "System Architect",
        "salary": "$3,120",
        "start_date": "Edinburgh",
        "office": "5421",
        "extn": "5421"},
        {
        "name": "testn",
        "position": "System Architect",
        "salary": "$3,120",
        "start_date": "Edinburgh",
        "office": "5421",
        "extn": "5421"},
        {
        "name": "testn",
        "position": "System Architect",
        "salary": "$3,120",
        "start_date": "Edinburgh",
        "office": "5421",
        "extn": "5421"},
        {
        "name": "testn",
        "position": "System Architect",
        "salary": "$3,120",
        "start_date": "Edinburgh",
        "office": "5421",
        "extn": "5421"},
        {
        "name": "testn",
        "position": "System Architect",
        "salary": "$3,120",
        "start_date": "Edinburgh",
        "office": "5421",
        "extn": "5421"},
        {
        "name": "testn",
        "position": "System Architect",
        "salary": "$3,120",
        "start_date": "Edinburgh",
        "office": "5421",
        "extn": "5421"},
        {
        "name": "testn",
        "position": "System Architect",
        "salary": "$3,120",
        "start_date": "Edinburgh",
        "office": "5421",
        "extn": "5421"},
        {
        "name": "testn",
        "position": "System Architect",
        "salary": "$3,120",
        "start_date": "Edinburgh",
        "office": "5421",
        "extn": "5421"}]
        print('post')
        return jsonify(dataset)
    else:
        pass




@travelExpenses.route('/travel_expenses_details/<int:month>/<int:travelExpensesId>')
@login_required
def travel_expenses_details(month, travelExpensesId):
    if travelExpensesId==None:
        print(travelExpensesId)
    else:
        _traTravelExpenses = TraTravelExpenses.query.get(travelExpensesId)

    detailsForm = TravelExpensesDetailsForm(_traTravelExpenses)
    return render_template('travel_expenses/travel-expenses-details.html', month=month, \
        travelExpensesId=travelExpensesId, detailsForm=detailsForm, activeSub='travelExpenses')


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
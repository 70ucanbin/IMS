from ims import db
from ims.service.mappers.models.traTravelExpenses import TraTravelExpenses as __model


# 1ヶ月分旅費精算リストを取得
def selectTraTravelExpensesList(employeeId, year, month):
    travelExpensesList = __model.query.filter_by(
        employee_id = employeeId,
        entry_year = year,
        entry_month = month
    ).all()

    return travelExpensesList

def selectTraTravelExpensesDetails(travelExpensesId, employeeId):
    query = __model.query.filter_by(
        employee_id = employeeId
    )
    dto = query.filter_by(entry_month = 9).all()
    dto = query.filter_by(
        travel_expenses_id = travelExpensesId
    ).first()

    return dto


def insertUpdateTraTravelExpenses(dto,isUpdate):

    model = __model()
    model.employee_id = dto['employeeId'],
    model.entry_year = dto['year'],
    model.entry_month = dto['month'],
    model.expense_date = dto['expenseDate'],
    model.expense_item = dto['expenseItem'],
    model.route = dto['route'],
    model.transit = dto['transit'],
    model.payment = dto['payment'],
    model.attached_file_id = dto['uploadFile'] or "",
    model.note = dto['note'] or ""

    if isUpdate:
        model.travel_expenses_id = dto['travelExpensesId']
        db.session.merge(model)
    else:
        db.session.add(model)
    db.session.flush()


def deleteTraTravelExpenses(travelExpensesId):

    result = __model.query.filter_by(travel_expenses_id = travelExpensesId).delete()

    db.session.flush()
    result = {'success':True}

    return result
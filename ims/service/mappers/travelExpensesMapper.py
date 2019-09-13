from ims import db
from ims.service.mappers.models.traTravelExpenses import TraTravelExpenses as __model


# 1ヶ月分旅費精算リストを取得
def selectTraTravelExpensesList(userId, year, month):
    travelExpensesList = __model.query.filter_by(
        user_id = userId,
        entry_year = year,
        entry_month = month
    ).all()

    return travelExpensesList

def selectTraTravelExpensesDetails(travelExpensesId, userId):
    query = __model.query.filter_by(
        user_id = userId
    )
    dto = query.filter_by(entry_month = 9).all()
    dto = query.filter_by(
        travel_expenses_id = travelExpensesId
    ).first()

    return dto


def insertUpdateTraTravelExpenses(dto,isUpdate):

    model = __model()
    model.user_id = dto['userId'],
    model.entry_year = dto['entryYear'],
    model.entry_month = dto['entryMonth'],
    model.expense_date = dto['expenseDate'],
    model.expense_item = dto['expenseItem'],
    model.route = dto['route'],
    model.transit = dto['transit'],
    model.payment = dto['payment'],
    model.file_name = dto['uploadFile'] or "",
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
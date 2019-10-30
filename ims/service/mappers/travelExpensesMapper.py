from ims import db
from ims.service.mappers.models.traTravelExpenses import TraTravelExpenses as __model


def selectTraTravelExpensesList(userId, year, month):
    """1ヶ月分旅費精算リストを取得するDB処理

    :param userId: 登録ユーザID
    :param year: 登録年
    :param month: 登録月
    """
    travelExpensesList = __model.query.filter_by(
        user_id = userId,
        entry_year = year,
        entry_month = month
    ).all()

    return travelExpensesList

def selectTraTravelExpensesDetails(travelExpensesId):
    """選択された旅費精算詳細を取得するDB処理

    :param travelExpensesId: 旅費精算ID
    """
    dto = __model.query.filter_by(
        travel_expenses_id = travelExpensesId
    ).first()

    return dto


def insertUpdateTraTravelExpenses(dto, isUpdate):
    """旅費精算を新規・修正するDB処理

    :param dto: 旅費精算詳細データ
    :param isUpdate: 新規・修正判定フラグ
    """
    model = __model()
    model.user_id = dto['userId'],
    model.entry_year = dto['entryYear'],
    model.entry_month = dto['entryMonth'],
    model.expense_date = dto['expenseDate'],
    model.expense_item = dto['expenseItem'],
    model.route = dto['route'],
    model.transit = dto['transit'],
    model.payment = dto['payment'],
    model.note = dto['note'] or ""

    if isUpdate:
        model.travel_expenses_id = dto['travelExpensesId']
        model.file_name = dto['uploadFile'],
        db.session.merge(model)
    else:
        db.session.add(model)
    db.session.flush()


def deleteTraTravelExpenses(travelExpensesId):
    """旅費精算を削除するDB処理

    :param travelExpensesId: 旅費精算ID
    """
    __model.query.filter_by(travel_expenses_id = travelExpensesId).delete()
    db.session.flush()
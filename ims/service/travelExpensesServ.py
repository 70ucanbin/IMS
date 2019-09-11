import traceback

from sqlalchemy.exc import IntegrityError

from ims import db
from ims.service.mappers.travelExpensesMapper import selectTraTravelExpensesList as __getList
from ims.service.mappers.travelExpensesMapper import selectTraTravelExpensesDetails as __getDetails
from ims.service.mappers.travelExpensesMapper import insertUpdateTraTravelExpenses as __insertUpdateOne
from ims.service.mappers.travelExpensesMapper import deleteTraTravelExpenses as __deleteOne


def getTravelExpensesList(employeeId, year, month):
    dto = __getList(employeeId, year, month)

    return dto

def getTravelExpensesDetails(travelExpensesId):
    """user情報を取得し、usernameを渡します
    """
    dto = __getDetails(travelExpensesId, 'k4111')

    return dto

def insertUpdateTravelExpenses(dto, isUpdate):
    try:
        __insertUpdateOne(dto,isUpdate)
        db.session.commit()
        result = {'success':True}
    except IntegrityError:
        traceback.print_exc()
        db.session.rollback()
        result = {'success':False,'message':'他のユーザが先に更新しました。'}
    finally: 
        db.session.close()
    return result


def deleteTravelExpenses(travelExpensesId):
    # try:
        result = __deleteOne(travelExpensesId)
        # if result['success'] == True:
        db.session.commit()
    #         return result
    #     else:
    # except Exception:
    #     traceback.print_exc()
    #     db.session.rollback()
    #     abort(404)
    # finally: 
        db.session.close()
        return result
import traceback

from flask import abort
from flask_login import current_user

from ims import db
from ims.service.mappers.comUserMapper import selectComUser as __getUser
from ims.service.mappers.travelExpensesMapper import selectTraTravelExpensesList as __getList
from ims.service.mappers.travelExpensesMapper import selectTraTravelExpensesDetails as __getDetails
from ims.service.mappers.travelExpensesMapper import insertUpdateTraTravelExpenses as __insertUpdateOne
from ims.service.mappers.travelExpensesMapper import deleteTraTravelExpenses as __deleteOne


def getTravelExpensesList(userId, year, month):
    """1ヶ月分旅費精算リストを取得するMapperを呼び出す

    :param userId: 登録ユーザID
    :param year: 登録年
    :param month: 登録月
    """
    dto = __getList(userId, year, month)

    return dto

def getTravelExpensesDetails(travelExpensesId):
    """選択された旅費精算詳細を取得するMapperを呼び出す

    :param travelExpensesId: 旅費精算ID
    """
    try:
        Id = int(travelExpensesId)
        dto = __getDetails(Id)
        if dto:
            user = __getUser(dto.user_id)
            if user.group_id == current_user.group_id:
                return dto
        else:
            return None
    except:
        return None

def insertUpdateTravelExpenses(dto, isUpdate):
    """旅費精算の新規または修正を処理するMapperを呼び出す
    サービス層のExceptionをキャッチし、処理します。

    :param dto: 旅費精算詳細データ
    :param isUpdate: 新規・修正判定フラグ
    """
    try:
        __insertUpdateOne(dto,isUpdate)
        db.session.commit()
    except Exception:
        traceback.print_exc()
        db.session.rollback()
        abort(500)
    finally: 
        db.session.close()


def deleteTravelExpenses(travelExpensesId):
    """旅費精算を削除するMapperを呼び出す
    サービス層のExceptionをキャッチし、処理します。

    :param travelExpensesId: 旅費精算ID
    """
    try:
        __deleteOne(travelExpensesId)
        db.session.commit()
    except Exception:
        traceback.print_exc()
        db.session.rollback()
        abort(500)
    finally: 
        db.session.close()
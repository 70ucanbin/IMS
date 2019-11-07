import traceback

from flask import abort
from flask_login import current_user

from sqlalchemy import exc

from ims import db
from ims.service.mappers.comUserMapper import selectComUser as __getUser
from ims.service.mappers.monthlyReportMapper import selectReportMonthDetails as __getMonthDetails
from ims.service.mappers.monthlyReportMapper import selectTraMonthlyReportDetails as __getDetails
from ims.service.mappers.monthlyReportMapper import insertUpdateTraMonthlyReport as __insertUpdateOne
from ims.service.mappers.monthlyReportMapper import insertDayOffFlg as __insertDayOff
from ims.service.mappers.monthlyReportMapper import deleteTraMonthlyReport as __deleteOne

def getMonthlyReportMonthDetails(userId, year, month, startDay, endDay):
    """1ヶ月分の日別稼働時間を取得するMapperを呼び出す

    :param userId: 登録ユーザID
    :param year: 登録年
    :param month: 登録月
    :param startDay: 月の初日
    :param endDay: 月の最後の日
    """
    result = __getMonthDetails(userId, year, month , startDay, endDay)

    return result

def getMonthlyReportDetails(userId, year, month, day):
    """選択された月報の詳細を取得するMapperを呼び出す

    :param userId: 登録ユーザID
    :param year: 登録年
    :param month: 登録月
    :param day: 登録日
    """
    dto = __getDetails(userId, year, month, day)
    if dto:
        user = __getUser(userId)
        if user.group_id == current_user.group_id:
            return dto
        else:
            return None
    else:
        return None

def insertUpdateMonthlyReport(dto, isUpdate):
    """月報詳細の新規または修正を処理するMapperを呼び出す
    サービス層のExceptionをキャッチし、処理します。

    :param dto: 月報詳細データ
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

def tookDayOff(year, month, day):
    """選択された日を休みとして登録するMapperを呼び出す
    サービス層のExceptionをキャッチし、処理します。

    :param year: 登録年
    :param month: 登録月
    :param day: 登録日
    """
    try:
        __deleteOne(current_user.user_id, year, month, day)
        __insertDayOff(current_user.user_id, year, month, day)
        db.session.commit()
    except Exception:
        traceback.print_exc()
        db.session.rollback()
        abort(500)
    finally: 
        db.session.close()

def deleteMonthlyReport(year, month, day):
    """月報詳細を削除するMapperを呼び出す
    サービス層のExceptionをキャッチし、処理します。

    :param year: 登録年
    :param month: 登録月
    :param day: 登録日
    """
    try:
        __deleteOne(current_user.user_id, year, month, day)
        db.session.commit()
    except Exception:
        traceback.print_exc()
        db.session.rollback()
        abort(500)
    finally: 
        db.session.close()
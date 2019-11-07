import traceback

from flask import abort
from flask_login import current_user

from sqlalchemy import exc

from ims import db
from ims.service.mappers.comUserMapper import selectComUser as __getUser
from ims.service.mappers.monthlyReportMapper import selectMonthlyReportDetails as __getMonthDetails
from ims.service.mappers.monthlyReportMapper import insertUpdateTraMonthlyReport as __insertUpdateOne

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

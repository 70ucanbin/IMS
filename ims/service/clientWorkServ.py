import traceback

from flask import abort
from flask_login import current_user

from sqlalchemy import exc

from ims import db
from ims.service.mappers.comUserMapper import selectComUser as __getUser
from ims.service.mappers.clientWorkMapper import selectWorkMonthDetails as __getMonthDetails
from ims.service.mappers.clientWorkMapper import selectTraClientWorkList as __getList
from ims.service.mappers.clientWorkMapper import selectTraClientWorkDetails as __getDetails
from ims.service.mappers.clientWorkMapper import insertUpdateTraClientWork as __insertUpdateOne
from ims.service.mappers.clientWorkMapper import insertDayOffFlg as __insertDayOff
from ims.service.mappers.clientWorkMapper import deleteTraClientWork as __deleteOne
from ims.service.mappers.clientWorkMapper import deleteDay as __deleteDay


def getClientWorkMonthDetails(userId, year, month, startDay, endDay):
    """1ヶ月分の日別稼働時間を取得するMapperを呼び出す

    :param userId: 登録ユーザID
    :param year: 登録年
    :param month: 登録月
    :param startDay: 月の初日
    :param endDay: 月の最後の日
    """
    result = __getMonthDetails(userId, year, month , startDay, endDay)

    return result

def getClientWorkList(userId, year, month, day):
    """選択された日の稼働リストを取得するMapperを呼び出す

    :param userId: 登録ユーザID
    :param year: 登録年
    :param month: 登録月
    :param day: 登録日
    """
    dto = __getList(current_user.group_id, userId, year, month ,day)

    return dto

def getClientWorkDetails(clientWorkId):
    """選択された稼働詳細を取得するMapperを呼び出す

    :param clientWorkId: 稼働詳細ID
    """
    try:
        Id = int(clientWorkId)
        dto = __getDetails(Id)
        if dto:
            user = __getUser(dto.userId)
            if user.group_id == current_user.group_id:
                return dto
            else:
                return None
        else:
            return None
    except:
        return None

def insertUpdateClientWork(dto, isUpdate):
    """稼働詳細の新規または修正を処理するMapperを呼び出す
    サービス層のExceptionをキャッチし、処理します。

    :param dto: 稼働詳細データ
    :param isUpdate: 新規・修正判定フラグ
    """
    try:
        __deleteDay(current_user.user_id, dto['year'], dto['month'], dto['day'])
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
        __deleteDay(current_user.user_id, year, month, day, 0)
        __insertDayOff(current_user.user_id, year, month, day)
        db.session.commit()
    except Exception:
        traceback.print_exc()
        db.session.rollback()
        abort(500)
    finally: 
        db.session.close()

def deleteClientWork(clientWorkId):
    """稼働詳細を削除するMapperを呼び出す
    サービス層のExceptionをキャッチし、処理します。

    :param clientWorkId: 稼働詳細ID
    """
    try:
        __deleteOne(clientWorkId)
        db.session.commit()
    except Exception:
        traceback.print_exc()
        db.session.rollback()
        abort(500)
    finally: 
        db.session.close()
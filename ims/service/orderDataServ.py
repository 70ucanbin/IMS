import traceback

from flask import abort
from flask_login import current_user

from sqlalchemy import exc

from ims import db
from ims.service.mappers.orderDataMapper import selectOrederList as __selectOrederList
from ims.service.mappers.orderDataMapper import selectOreder as __selectOreder
from ims.service.mappers.orderDataMapper import checkUnique as __checkUnique
from ims.service.mappers.orderDataMapper import insertUpdateOreder as __insertUpdateOreder
from ims.service.mappers.orderDataMapper import deleteOreder as __deleteOreder


def getOrderList(groupCd):
    """件名大分類リストを取得するMapperを呼び出す

    :param clientCd: クライアントコード
    :param groupCd: 所属コード
    :param orderCd: オーダーコード
    """
    dtoList = __selectOrederList(groupCd)

    return dtoList

def getOrderDetails(orderId):
    result = __selectOreder(orderId)

    return result

def checkUnique(clientCd, groupCd, orderCd):
    result = __checkUnique(clientCd, groupCd, orderCd)

    return result

def insertUpdateOrder(dto, isUpdate):
    """大分類詳細の新規または修正を処理するMapperを呼び出す
    サービス層のExceptionをキャッチし、処理します。

    :param dto: 大分類詳細データ
    :param isUpdate: 新規・修正判定フラグ
    """
    try:
        __insertUpdateOreder(dto,isUpdate)
        db.session.commit()
    except Exception:
        traceback.print_exc()
        db.session.rollback()
        abort(500)
    finally: 
        db.session.close()

def deleteOrder(orderId):
    """大分類データを削除するMapperを呼び出す
    サービス層のExceptionをキャッチし、処理します。

    :param itemId: 大分類データID
    """
    try:
        __deleteOreder(orderId)
        db.session.commit()
    except Exception:
        traceback.print_exc()
        db.session.rollback()
        abort(500)
    finally: 
        db.session.close()

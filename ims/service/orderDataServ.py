import traceback

from flask import abort
from flask_login import current_user

from sqlalchemy import exc

from ims import db
from ims.service.mappers.orderDataMapper import checkUnique as __checkUnique
from ims.service.mappers.orderDataMapper import selectOrederList as __selectOrederList
from ims.service.mappers.orderDataMapper import selectSubOrederList as __selectSubOrederList
from ims.service.mappers.orderDataMapper import selectOreder as __selectOreder
from ims.service.mappers.orderDataMapper import selectSubOreder as __selectSubOreder
from ims.service.mappers.orderDataMapper import insertUpdateOreder as __insertUpdateOreder
from ims.service.mappers.orderDataMapper import insertUpdateSubOreder as __insertUpdateSubOreder
from ims.service.mappers.orderDataMapper import deleteOreder as __deleteOreder
from ims.service.mappers.orderDataMapper import deleteSubOreder as __deleteSubOreder


def getOrderList(groupCd):
    """件名大分類リストを取得するMapperを呼び出す

    :param groupCd: 所属コード
    """
    dtoList = __selectOrederList(groupCd)

    return dtoList

def getOrderDetails(orderId):
    """件名大分類詳細を取得するMapperを呼び出す

    :param orderId: 対象コードID
    """
    result = __selectOreder(orderId)

    return result

def checkUnique(clientCd, groupCd, orderCd, subOrderCd):
    """件名大分類・小分類の一意制約をチェックするMapperを呼び出す

    :param clientCd: クライアントコード
    :param groupCd: 所属コード
    :param orderCd: オーダーコード
    :param subOrderCd: サブオーダーコード
    """
    result = __checkUnique(clientCd, groupCd, orderCd, subOrderCd)

    return result

def insertUpdateOrder(dto, isUpdate):
    """大分類詳細の新規または修正を処理するMapperを呼び出す
    サービス層のExceptionをキャッチし、処理します。

    :param dto: 大分類詳細データ
    :param isUpdate: 新規・修正判定フラグ
    """
    try:
        __insertUpdateOreder(dto, isUpdate)
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

    :param orderId: 大分類データID
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

def getSubOrderList(groupCd, orderCd):
    """件名小分類リストを取得するMapperを呼び出す

    :param groupCd: 所属コード
    :param orderCd: オーダーコード
    """
    dtoList = __selectSubOrederList(groupCd, orderCd)

    return dtoList

def getSubOrderDetails(subOrderId):
    result = __selectSubOreder(subOrderId)

    return result

def insertUpdateSubOrder(dto, isUpdate):
    """件名小分類詳細の新規または修正を処理するMapperを呼び出す
    サービス層のExceptionをキャッチし、処理します。

    :param dto: 小分類詳細データ
    :param isUpdate: 新規・修正判定フラグ
    """
    try:
        __insertUpdateSubOreder(dto, isUpdate)
        db.session.commit()
    except Exception:
        traceback.print_exc()
        db.session.rollback()
        abort(500)
    finally: 
        db.session.close()

def deleteSubOrder(subOrderId):
    """小分類データを削除するMapperを呼び出す
    サービス層のExceptionをキャッチし、処理します。

    :param subOrderId: 大分類データID
    """
    try:
        __deleteSubOreder(subOrderId)
        db.session.commit()
    except Exception:
        traceback.print_exc()
        db.session.rollback()
        abort(500)
    finally: 
        db.session.close()

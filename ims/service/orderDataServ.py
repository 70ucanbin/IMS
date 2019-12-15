import traceback

from flask import abort, flash
from flask_login import current_user

from sqlalchemy.exc import IntegrityError

from ims import db
from ims.common.Messages import Messages
from ims.service.mappers.orderDataMapper import selectOrederList as __selectOrederList
from ims.service.mappers.orderDataMapper import selectSubOrederList as __selectSubOrederList
from ims.service.mappers.orderDataMapper import selectOreder as __selectOreder
from ims.service.mappers.orderDataMapper import selectSubOreder as __selectSubOreder
from ims.service.mappers.orderDataMapper import insertUpdateOreder as __insertUpdateOreder
from ims.service.mappers.orderDataMapper import insertUpdateSubOreder as __insertUpdateSubOreder
from ims.service.mappers.orderDataMapper import deleteOreder as __deleteOreder
from ims.service.mappers.orderDataMapper import deleteSubOreder as __deleteSubOreder


def getOrderList(groupId):
    """件名大分類リストを取得するMapperを呼び出す

    :param groupId: 所属コード
    """
    dtoList = __selectOrederList(groupId)
    return dtoList

def getOrderDetails(orderId):
    """件名大分類詳細を取得するMapperを呼び出す

    :param orderId: 対象コードID
    """
    result = __selectOreder(orderId)

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
    except IntegrityError:
        flash(Messages.WARNING_UNIQUE_CONSTRAINT, Messages.WARNING_CSS)
        raise IntegrityError
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

def getSubOrderList(groupId, orderCd):
    """件名小分類リストを取得するMapperを呼び出す

    :param groupId: 所属コード
    :param orderCd: オーダーコード
    """
    dtoList = __selectSubOrederList(groupId, orderCd)

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
    except IntegrityError:
        flash(Messages.WARNING_UNIQUE_CONSTRAINT, Messages.WARNING_CSS)
        raise IntegrityError
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

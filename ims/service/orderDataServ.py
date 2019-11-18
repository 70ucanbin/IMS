import traceback

from flask import abort
from flask_login import current_user

from sqlalchemy import exc

from ims import db
from ims.service.mappers.orderDataMapper import selectOrederList as __selectOrederList
from ims.service.mappers.comItemMapper import selectComItem as __selectItem

from ims.service.mappers.comItemMapper import insertUpdateComItem as __insertUpdateItem
from ims.service.mappers.comItemMapper import deleteComItem as __deleteOne


def getOrderList(groupCd):
    """件名大分類リストを取得するMapperを呼び出す

    :param clientCd: クライアントコード
    :param groupCd: 所属コード
    :param orderCd: オーダーコード
    """
    dtoList = __selectOrederList(groupCd)

    return dtoList

def insertUpdateOrderData(dto, isUpdate):
    """大分類詳細の新規または修正を処理するMapperを呼び出す
    サービス層のExceptionをキャッチし、処理します。

    :param dto: 大分類詳細データ
    :param isUpdate: 新規・修正判定フラグ
    """
    try:
        __insertUpdateItem(dto,isUpdate)
        db.session.commit()
    except Exception:
        traceback.print_exc()
        db.session.rollback()
        abort(500)
    finally: 
        db.session.close()

def deleteOrderData(orderId):
    """大分類データを削除するMapperを呼び出す
    サービス層のExceptionをキャッチし、処理します。

    :param itemId: 大分類データID
    """
    try:
        __deleteOne(itemId)
        db.session.commit()
    except Exception:
        traceback.print_exc()
        db.session.rollback()
        abort(500)
    finally: 
        db.session.close()

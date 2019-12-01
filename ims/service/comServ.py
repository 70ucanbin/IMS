import traceback

from flask import abort

from sqlalchemy import exc

from ims import db
from ims.service.mappers.comItemMapper import selectComItemList as __selectItemList
from ims.service.mappers.comItemMapper import selectComItem as __selectItem
from ims.service.mappers.comItemMapper import checkUnique as __checkUnique
from ims.service.mappers.comItemMapper import insertUpdateComItem as __insertUpdateItem
from ims.service.mappers.comItemMapper import deleteComItem as __deleteComItem

from ims.service.mappers.comUserMapper import selectComUser, insertComUser, selectComUserList


def getComItem(itemId):
    """マスタデータ詳細を取得するMapperを呼び出す

    :param itemId: マスタデータID
    """
    result = __selectItem(itemId)

    return result

def checkUnique(itemCategory, itemCd):
    """マスタデータ一意制約のチェックを処理するMapperを呼び出す

    :param itemCategory: カテゴリー
    :param itemCd: コード
    """
    result = __checkUnique(itemCategory,itemCd)

    return result

def insertUpdateMasterData(dto, isUpdate):
    """マスタデータ詳細の新規または修正を処理するMapperを呼び出す
    サービス層のExceptionをキャッチし、処理します。

    :param dto: マスタデータ詳細データ
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

def deleteMasterData(itemId):
    """マスタデータを削除するMapperを呼び出す
    サービス層のExceptionをキャッチし、処理します。

    :param itemId: マスタデータID
    """
    try:
        __deleteComItem(itemId)
        db.session.commit()
    except Exception:
        traceback.print_exc()
        db.session.rollback()
        abort(500)
    finally: 
        db.session.close()

def getComItemList(category):
    result = __selectItemList(category)

    return result

def getComUserList(groupId):
    result = selectComUserList(groupId)

    return result

def getComUser(userId):
    result = selectComUser(userId)

    return result

def insertUpdateComUser(dto):
    insertComUser(dto)
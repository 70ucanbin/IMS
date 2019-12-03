import traceback

from flask import abort
from flask_login import current_user

from sqlalchemy import exc

from ims import db
from ims.service.mappers.comItemMapper import selectComItemList as __selectItemList
from ims.service.mappers.comItemMapper import selectComItem as __selectItem
from ims.service.mappers.comItemMapper import checkUnique as __checkUnique
from ims.service.mappers.comItemMapper import insertUpdateComItem as __insertUpdateItem
from ims.service.mappers.comItemMapper import deleteComItem as __deleteItem
from ims.service.mappers.comUserMapper import selectComUserList as __selectUserList
from ims.service.mappers.comUserMapper import selectComUser as __selectUser
from ims.service.mappers.comUserMapper import insertComUser as __insertUser


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
        __deleteItem(itemId)
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
    """選択された所属ユーザー情報のリストを取得を処理するMapperを呼び出す
    サービス層のExceptionをキャッチし、処理します。

    :param groupId: 所属ID
    """
    result = __selectUserList(groupId)

    return result

def getComUser(userId):
    """ユーザー情報を取得を処理するMapperを呼び出す
    サービス層のExceptionをキャッチし、処理します。

    :param userId: ユーザーデータID
    """
    result = __selectUser(userId)

    return result

def insertUpdateComUser(dto, isUpdate):
    """ユーザー情報の新規または修正を処理するMapperを呼び出す
    サービス層のExceptionをキャッチし、処理します。

    :param dto: ユーザー情報詳細データ
    :param isUpdate: 新規・修正判定フラグ
    """
    try:
        __insertUser(dto, isUpdate, current_user.user_id)
        db.session.commit()
    except Exception:
        traceback.print_exc()
        db.session.rollback()
        abort(500)
    finally: 
        db.session.close()

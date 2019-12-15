import traceback

from flask import abort, flash
from flask_login import current_user

from sqlalchemy.exc import IntegrityError

from ims import db
from ims.common.Messages import Messages
from ims.service.mappers.comItemMapper import selectComItemList as __selectItemList
from ims.service.mappers.comItemMapper import selectComItem as __selectItem
from ims.service.mappers.comItemMapper import insertUpdateComItem as __insertUpdateItem
from ims.service.mappers.comItemMapper import deleteComItem as __deleteItem
from ims.service.mappers.comUserMapper import selectComUserList as __selectUserList
from ims.service.mappers.comUserMapper import selectAllUserList as __selectAllUserList
from ims.service.mappers.comUserMapper import selectComUser as __selectUser
from ims.service.mappers.comUserMapper import insertUpdateComUser as __insertUpdateUser


def getComItem(itemId):
    """マスタデータ詳細を取得するMapperを呼び出す

    :param itemId: マスタデータID
    """
    result = __selectItem(itemId)

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
    except IntegrityError:
        flash(Messages.WARNING_UNIQUE_CONSTRAINT, Messages.WARNING_CSS)
        raise IntegrityError
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
    """選択された所属のユーザー情報リストを取得を処理するMapperを呼び出す
    サービス層のExceptionをキャッチし、処理します。

    :param groupId: 所属ID
    """
    result = __selectUserList(groupId)

    return result

def getAllUserList():
    """すべてのユーザー情報リストを取得を処理するMapperを呼び出す
    サービス層のExceptionをキャッチし、処理します。

    """
    result = __selectAllUserList()

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
        __insertUpdateUser(dto, isUpdate, current_user.user_id)
        db.session.commit()
    except Exception:
        traceback.print_exc()
        db.session.rollback()
        abort(500)
    finally: 
        db.session.close()

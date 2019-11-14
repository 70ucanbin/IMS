import traceback

from flask import abort
from flask_login import current_user

from sqlalchemy import exc

from ims import db
from ims.service.mappers.comItemMapper import selectComItemList, selectComItemList2
from ims.service.mappers.comItemMapper import insertUpdateComItem as __insertUpdateOne

from ims.service.mappers.comUserMapper import selectComUser, insertComUser, selectComUserList

# 業務コンボボックスListを取得する
def getComItemList(category):
    result = selectComItemList(category)

    return result

def insertUpdateMasterData(dto, isUpdate):
    """マスタデータ詳細の新規または修正を処理するMapperを呼び出す
    サービス層のExceptionをキャッチし、処理します。

    :param dto: マスタデータ詳細データ
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

def getCategoryList(category):
    result = selectComItemList2(category)

    return result

def getComUserList(groupId):
    result = selectComUserList(groupId)

    return result

def getComUser(userId):
    result = selectComUser(userId)

    return result

def insertUpdateComUser(dto):
    insertComUser(dto)
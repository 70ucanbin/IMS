from sqlalchemy import and_
from sqlalchemy.orm import aliased

from ims import db
from ims.service.mappers.models.comUser import User as __model
from ims.service.mappers.models.comItem import ComItem


def selectComUserList(groupId):
    groupName = aliased(ComItem)
    dto = db.session.query(
        __model.user_id.label('userId'),
        __model.user_name.label('userName'),
        groupName.item_value.label('groupName'),
        __model.email.label('email')
    ).filter(
        __model.group_id == groupId
    ).outerjoin(
        (groupName, 
        and_(groupName.item_category == 'group_id',
        groupName.item_cd == __model.group_id))
    ).all()
    return dto

def selectComUser(userId):
    dto = __model.query.filter_by(
        user_id = userId
    ).first()
    return dto

def insertComUser(dto, isUpdate, updateUser):
    """ユーザー情報を新規・修正するDB処理

    :param dto: ユーザー情報詳細データ
    :param isUpdate: 新規・修正判定フラグ
    :param updateUser: 更新ユーザーID
    """
    model = __model()
    model.user_id = dto['userId']
    model.user_name = dto['userName']
    model.password = dto['password']
    model.group_id = dto['groupId']
    model.user_role = dto['role']
    model.email = dto['email']
    model.update_user = updateUser

    if isUpdate:
        model.user_id = dto['userId']
        db.session.merge(model)
    else:
        db.session.add(model)
    db.session.flush()
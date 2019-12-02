from ims import db
from ims.service.mappers.models.comUser import User as __model


def selectComUserList(groupId):
    dto = __model.query.filter_by(
        group_id = groupId
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
    model.is_manager = dto['role']
    model.email = dto['email']
    model.update_user = updateUser

    if isUpdate:
        model.user_id = dto['userId']
        db.session.merge(model)
    else:
        db.session.add(model)
    db.session.flush()
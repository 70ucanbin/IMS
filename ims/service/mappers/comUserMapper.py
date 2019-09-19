from ims import db
from ims.service.mappers.models.comUser import User as __model

def selectComUser(userId):
    dto = __model.query.filter_by(
        user_id = userId
    ).first()
    return dto

def insertComUser(dto):
    model = __model()
    model.user_id = dto['userId']
    model.password = dto['password']
    db.session.add(model)
    db.session.commit()


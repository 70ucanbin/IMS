from ims.service.mappers.comItemMapper import selectComItemList
from ims.service.mappers.comUserMapper import selectComUser, insertComUser

# 業務コンボボックスListを取得する
def getComItemList(category):
    result = selectComItemList(category)

    return result

def getComUser(userId):
    result = selectComUser(userId)

    return result

def insertUpdateComUser(dto):
    insertComUser(dto)
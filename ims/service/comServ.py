from ims.service.mappers.comItemMapper import selectComItemList, selectComItemList2
from ims.service.mappers.comUserMapper import selectComUser, insertComUser, selectComUserList

# 業務コンボボックスListを取得する
def getComItemList(category):
    result = selectComItemList(category)

    return result

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
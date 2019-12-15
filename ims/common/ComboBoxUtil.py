from ims.service.comServ import getComUserList

class _SelectBox:
    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value

# 同じ組織IDのユーザリストを取得するため、組織判定が必要
def getUserList(groupId):
    userList = getComUserList(groupId)
    result = [_SelectBox(user.userId, user.userName) for user in userList]
    return result

def getNumberList(startingPoint, endPoint, step):
    _NumberRange = list(range(startingPoint, endPoint, step))
    numberList = list()

    for number in _NumberRange:
        numberList.append(_SelectBox(number, number))
    return numberList

        # selectList.append(_SelectBox(minutes, str(minutes).zfill(2)))

def getComItem(dataSet):
    itemList = list()
    itemList.append(_SelectBox('',''))
    for data in dataSet:
        itemList.append(_SelectBox(data.item_key,data.item_key + ' ' + data.item_value))

    return itemList

def getComCategoryList(dataSet):
    categoryList = list()
    for data in dataSet:
        categoryList.append(_SelectBox(data.item_cd, data.item_value))
    categoryList.append(_SelectBox('master_combo', '基本情報'))
    return categoryList

def getOrderComBoList(dataSet, init_flg=False):
    orderList = list()
    if init_flg:
        orderList.append(_SelectBox('',''))
    for data in dataSet:
        orderList.append(_SelectBox(data.orderCd, data.orderValue))

    return orderList
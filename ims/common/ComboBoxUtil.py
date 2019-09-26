
class _SelectBox:
    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value

# 同じ組織IDのユーザリストを取得するため、組織判定が必要
def getUserList(dto):
    userList = list()
    for user in dto:
        userList.append(_SelectBox(user.user_id, user.user_name))
    return userList

def getNumberList(startingPoint, endPoint, step):
    _NumberRange = list(range(startingPoint, endPoint, step))
    numberList = list()

    for number in _NumberRange:
        numberList.append(_SelectBox(number, number))
    return numberList

        # selectList.append(_SelectBox(minutes, str(minutes).zfill(2)))

def getComItem(dataSet):
    itemList = list()
    for data in dataSet:
        itemList.append(_SelectBox(data.item_key,data.item_key + ' ' + data.item_value))

    return itemList
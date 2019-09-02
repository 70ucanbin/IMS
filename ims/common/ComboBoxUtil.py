
class _SelectBox:
    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value

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
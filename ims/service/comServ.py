from ims.service.mappers.comItemMapper import selectComItemList

# 業務コンボボックスListを取得する
def getComItemList(category):
    result = selectComItemList(category)

    return result

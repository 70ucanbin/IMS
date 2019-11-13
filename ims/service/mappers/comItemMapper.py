from ims.service.mappers.models.comItem import ComItem ,ComItem2

def selectComItemList(category):
    dto = ComItem.query.filter_by(
        item_category=category
    ).all()

    return dto

def selectComItemList2(category):
    dto = ComItem2.query.filter_by(
        item_category=category
    ).all()

    return dto
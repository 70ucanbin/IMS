from ims.service.mappers.models.comItem import ComItem

def selectComItemList(category):
    dto = ComItem.query.filter_by(
        item_category=category
    ).all()

    return dto
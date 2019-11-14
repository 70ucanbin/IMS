from ims import db
from ims.service.mappers.models.comItem import ComItem
from ims.service.mappers.models.comItem import ComItem2 as __model

def selectComItemList(category):
    dto = ComItem.query.filter_by(
        item_category=category
    ).all()

    return dto

def selectComItemList2(category):
    dto = __model.query.filter_by(
        item_category=category
    ).all()

    return dto

def insertUpdateComItem(dto, isUpdate):
    """マスタデータ詳細の新規または修正を処理するDB処理

    :param dto: マスタデータ詳細データ
    :param isUpdate: 新規・修正判定フラグ
    """
    model = __model()
    model.item_category = dto['itemCategory'],
    model.item_cd = dto['itemCD'],
    model.item_value = dto['itemValue'],
    model.display_order = dto['displayOrder'],
    # model.is_active = True,
    model.update_user = dto['updateUser']
    # model.update_date = dto['updateDate']

    if isUpdate:
        db.session.merge(model)
    else:
        db.session.add(model)
    db.session.flush()
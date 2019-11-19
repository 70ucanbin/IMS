from ims import db
from ims.service.mappers.models.comItem import ComItem
from ims.service.mappers.models.comItem import ComItem2 as __model


def selectComItemList(category):
    dto = ComItem.query.filter_by(
        item_category = category
    ).all()

    return dto

def selectComItemList2(category):
    dto = __model.query.filter_by(
        item_category = category
    ).order_by(
        __model.display_order
    ).all()

    return dto

def selectComItem(itemId):
    dto = __model.query.filter_by(
        item_id = itemId
    ).first()

    return dto

def checkUnique(itemCategory, itemCd):
    """マスタデータ一意制約をチェックするDB処理

    :param itemCategory: カテゴリー
    :param itemCd: コード
    """
    dto = __model.query.filter_by(
        item_category = itemCategory,
        item_cd = itemCd
    ).first()

    if dto:
        return False
    else:
        return True

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
    if dto['isActive'] == True:
        model.is_active = True
    else:
        model.is_active = False
    model.update_user = dto['updateUser']
    # model.update_date = dto['updateDate']

    if isUpdate:
        model.item_id = dto['itemId']
        db.session.merge(model)
    else:
        db.session.add(model)
    db.session.flush()

def deleteComItem(itemId):
    """マスタデータを削除するDB処理

    :param itemId: マスタデータID
    """
    __model.query.filter_by(item_id = itemId).delete()
    db.session.flush()
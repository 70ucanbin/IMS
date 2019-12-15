from ims import db
from ims.service.mappers.models.comItem import ComItem as __model


def selectComItemList(category):
    """マスタデータListを取得するDB処理

    :param category: データカテゴリー
    """
    dto = __model.query.filter_by(
        item_category = category
    ).order_by(
        __model.display_order
    ).all()

    return dto

def selectComItem(itemId):
    """マスタデータ詳細を取得するDB処理

    :param itemId: マスタデータID
    """
    dto = __model.query.filter_by(
        item_id = itemId
    ).first()

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
    if dto['isActive'] == True:
        model.is_active = True
    else:
        model.is_active = False
    model.update_user = dto['updateUser']

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
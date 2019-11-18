from ims import db
from ims.service.mappers.models.traOrderData import TraOrder as __orderModel


def selectOrederList(groupCd):
    """件名大分類リストを取得するDB処理

    :param clientCd: クライアントコード
    :param groupCd: 所属コード
    :param orderCd: オーダーコード
    """
    orderList = __orderModel.query.filter_by(
        group_cd = groupCd
    ).all()

    return orderList













def insertUpdateComItem(dto, isUpdate):
    """マスタデータ詳細の新規または修正を処理するDB処理

    :param dto: マスタデータ詳細データ
    :param isUpdate: 新規・修正判定フラグ
    """
    model = __orderModel()
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
    __orderModel.query.filter_by(item_id = itemId).delete()
    db.session.flush()
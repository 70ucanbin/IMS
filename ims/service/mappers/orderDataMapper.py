from sqlalchemy import and_
from sqlalchemy.orm import aliased

from ims import db
from ims.service.mappers.models.comItem import ComItem2
from ims.service.mappers.models.traOrderData import TraOrder as __orderModel


def selectOrederList(groupCd):
    """件名大分類リストを取得するDB処理

    :param groupCd: 所属コード
    """
    client_name = aliased(ComItem2)

    orderList = db.session.query(
        __orderModel.order_id.label('orderId'),
        client_name.item_value.label('clientName'),
        __orderModel.order_cd.label('orderCd'),
        __orderModel.order_value.label('orderValue'),
        __orderModel.display_order.label('displayOrder'),
        __orderModel.is_active.label('isActive'),
    ).filter(
        __orderModel.group_cd == groupCd
    ).outerjoin(
        (client_name,
        and_(client_name.item_cd == __orderModel.client_cd,
        client_name.item_category =='client_cd'))
    ).all()

    return orderList

def selectOreder(orderId):
    """件名大分類詳細を取得するDB処理

    :param orderId: オーダーID
    """
    dto = __orderModel.query.filter_by(
        order_id = orderId
    ).first()

    return dto

def checkUnique(clientCd, groupCd, orderCd):
    """件名大分類詳細一意制約をチェックするDB処理

    :param clientCd: クライアントコード
    :param groupCd: 所属コード
    :param orderCd: オーダーコード
    """
    dto = __orderModel.query.filter_by(
        client_cd = clientCd,
        group_cd = groupCd,
        order_cd = orderCd
    ).first()

    if dto:
        return False
    else:
        return True

def insertUpdateOreder(dto, isUpdate):
    """件名大分類詳細の新規または修正を処理するDB処理

    :param dto: 件名大分類詳細データ
    :param isUpdate: 新規・修正判定フラグ
    """
    model = __orderModel()
    model.client_cd = dto['clientCd'],
    model.group_cd = dto['groupCd'],
    model.order_cd = dto['orderCd'],
    model.order_value = dto['orderValue'],
    model.display_order = dto['displayOrder'],
    if dto['isActive'] == True:
        model.is_active = True
    else:
        model.is_active = False
    model.update_user = dto['updateUser']

    if isUpdate:
        model.order_id = dto['orderId']
        db.session.merge(model)
    else:
        db.session.add(model)
    db.session.flush()

def deleteOreder(orderId):
    """件名大分類データを削除するDB処理

    :param orderId: 件名大分類データID
    """
    __orderModel.query.filter_by(order_id = orderId).delete()
    db.session.flush()
from sqlalchemy import and_
from sqlalchemy.orm import aliased

from ims import db
from ims.service.mappers.models.comItem import ComItem
from ims.service.mappers.models.traOrderData import TraOrder as __orderModel
from ims.service.mappers.models.traOrderData import TraSubOrder as __subOrderModel


def selectOrederList(groupId):
    """件名大分類リストを取得するDB処理

    :param groupId: 所属コード
    """
    client_name = aliased(ComItem)

    orderList = db.session.query(
        __orderModel.order_id.label('orderId'),
        client_name.item_value.label('clientName'),
        __orderModel.order_cd.label('orderCd'),
        __orderModel.order_value.label('orderValue'),
        __orderModel.display_order.label('displayOrder'),
        __orderModel.is_active.label('isActive'),
    ).filter(
        __orderModel.group_id == groupId
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

def insertUpdateOreder(dto, isUpdate):
    """件名大分類詳細の新規または修正を処理するDB処理

    :param dto: 件名大分類詳細データ
    :param isUpdate: 新規・修正判定フラグ
    """
    model = __orderModel()
    model.client_cd = dto['clientCd'],
    model.group_id = dto['groupId'],
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

def selectSubOrederList(groupId, orderCd):
    """件名小分類リストを取得するDB処理

    :param groupId: 所属コード
    :param orderCd: オーダーコード
    """
    client_name = aliased(ComItem)

    orderList = db.session.query(
        __subOrderModel.sub_order_id.label('orderId'),
        client_name.item_value.label('clientName'),
        __subOrderModel.sub_order_cd.label('subOrderCd'),
        __subOrderModel.sub_order_value.label('subOrderValue'),
        __subOrderModel.display_order.label('displayOrder'),
        __subOrderModel.is_active.label('isActive'),
    ).filter(
        __subOrderModel.group_id == groupId,
        __subOrderModel.order_cd == orderCd
    ).outerjoin(
        (client_name,
        and_(client_name.item_cd == __subOrderModel.client_cd,
        client_name.item_category =='client_cd'))
    ).all()

    return orderList

def selectSubOreder(subOrderId):
    """件名小分類詳細を取得するDB処理

    :param orderId: オーダーID
    """
    dto = __subOrderModel.query.filter_by(
        sub_order_id = subOrderId
    ).first()

    return dto

def insertUpdateSubOreder(dto, isUpdate):
    """件名小分類詳細の新規または修正を処理するDB処理

    :param dto: 件名小分類詳細データ
    :param isUpdate: 新規・修正判定フラグ
    """
    model = __subOrderModel()
    model.client_cd = dto['clientCd'],
    model.group_id = dto['groupId'],
    model.order_cd = dto['orderCd'],
    model.sub_order_cd = dto['subOrderCd'],
    model.sub_order_value = dto['subOrderValue'],
    model.display_order = dto['displayOrder'],
    if dto['isActive'] == True:
        model.is_active = True
    else:
        model.is_active = False
    model.update_user = dto['updateUser']

    if isUpdate:
        model.sub_order_id = dto['subOrderId']
        db.session.merge(model)
    else:
        db.session.add(model)
    db.session.flush()

def deleteSubOreder(subOrderId):
    """件名小分類データを削除するDB処理

    :param subOrderId: 件名小分類データID
    """
    __subOrderModel.query.filter_by(sub_order_id = subOrderId).delete()
    db.session.flush()

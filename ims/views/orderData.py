from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for, session
from flask_login import login_required, current_user

from ims.common.ComboBoxUtil import getOrderComBoList
from ims.common.Messages import Messages
from ims.contents.orderDataCont import OrderDataList as orderListCont
from ims.contents.orderDataCont import Details as detailsCont
from ims.contents.orderDataCont import SubOrderDataList as subOrderListCont

from ims.form.orderDataForm import OrderDataForm, SubOrderDataForm
from ims.service.comServ import getComItemList2
from ims.service.orderDataServ import getOrderList
from ims.service.orderDataServ import getSubOrderList
from ims.service.orderDataServ import getOrderDetails
from ims.service.orderDataServ import getSubOrderDetails
from ims.service.orderDataServ import checkUnique
from ims.service.orderDataServ import insertUpdateOrder
from ims.service.orderDataServ import insertUpdateSubOrder
from ims.service.orderDataServ import deleteOrder
from ims.service.orderDataServ import deleteSubOrder

orderData = Blueprint('orderData', __name__)


@orderData.route('/order_list/')
@login_required
def order_list():
    """件名大分類データ一覧の初期表示  GETのrequestを受付
    当処理はhtmlテンプレート及び画面用コンテンツを返します。
    """
    data = getOrderList(current_user.group_id)
    cont = orderListCont(data)
    return render_template('order_data_management/order-list.html', cont=cont)


@orderData.route('/order_create/')
@login_required
def order_create():
    """件名大分類データ作成処理
    
    件名大分類一覧画面から「新規作成」を押下後、GETのrequestを受付します。
    htmlテンプレート及び画面用コンテンツを返します。
    """
    clientList = getComItemList2('client_cd')
    form = OrderDataForm()
    form.clientCd.choices = [(i.item_cd, i.item_value) for i in clientList]
    cont = detailsCont(form)
    return render_template('order_data_management/order-details.html', cont=cont)


@orderData.route('/order/<int:orderId>/edit/')
@login_required
def order_edit(orderId):
    """件名大分類データ修正処理
    
    一覧画面からデータの「コード」を押下後、GETのrequestを受付します。
    htmlテンプレート及び画面用コンテンツを返します。

    :param orderId: 選択された件名大分類データのID
    """
    dto = getOrderDetails(orderId)
    if not dto:
        flash(Messages.WARNING_NOT_FOUND_ALREADY_UPDATED_DELETED, 
            Messages.WARNING_CSS)
        return redirect(url_for('orderData.order_list'))

    clientList = getComItemList2('client_cd')
    form = OrderDataForm()
    form.clientCd.choices = [(i.item_cd, i.item_value) for i in clientList]
    form.orderId.data = dto.order_id
    form.clientCd.data = dto.client_cd
    form.orderCd.data = dto.order_cd
    form.orderValue.data = dto.order_value
    form.displayOrder.data = dto.display_order
    form.isActive.data = dto.is_active

    cont = detailsCont(form)
    return render_template('order_data_management/order-details.html', cont=cont)


@orderData.route('/order_details/save/', methods=['POST'])
@login_required
def order_save():
    """件名大分類データ詳細画面登録処理

    formのデータをDBに保存します。
    処理終了後はマスタデータ一覧画面へ遷移します。
    """
    clientList = getComItemList2('client_cd')
    form = OrderDataForm()
    form.clientCd.choices = [(i.item_cd, i.item_value) for i in clientList]
    if form.validate_on_submit():
        if form.orderId.data:
            isUpdate = True
            dto = getOrderDetails(form.orderId.data)
            if dto:
                pass
            else:
                flash(Messages.WARNING_NOT_FOUND_ALREADY_UPDATED_DELETED, 
                    Messages.WARNING_CSS)
                return redirect(url_for('orderData.order_list'))
        else:
            isUpdate = False
            result = checkUnique(
                form.clientCd.data,
                current_user.group_id,
                form.orderCd.data,
                None
                )
            if result:
                pass
            else:
                flash(Messages.WARNING_UNIQUE_CONSTRAINT, Messages.WARNING_CSS)
                return redirect(url_for('orderData.order_list'))
        data = form.data
        data['groupCd'] = current_user.group_id
        data['updateUser'] = current_user.user_id
        data['isActive'] = bool(form.isActive.data)

        insertUpdateOrder(data, isUpdate)
        if isUpdate:
            flash(Messages.SUCCESS_UPDATED, Messages.SUCCESS_CSS)
        else:
            flash(Messages.SUCCESS_INSERTED, Messages.SUCCESS_CSS)
        return redirect(url_for('orderData.order_list'))

    for error in form.errors.values():
        flash(error[0],Messages.DANGER_CSS)

    cont = detailsCont(form)

    return render_template('order_data_management/order-details.html', cont=cont)


@orderData.route('/order_details/<int:orderId>/delete/')
@login_required
def order_delete(orderId):
    """件名大分類データ詳細画面削除処理

    当該データを物理削除します。
    処理終了後は件名大分類データ一覧画面へ遷移します。

    :param orderId: 削除対象のIDです。
    """
    dto = getOrderDetails(orderId)
    if dto:
        pass
    else:
        flash(Messages.WARNING_NOT_FOUND_ALREADY_UPDATED_DELETED, 
            Messages.WARNING_CSS)
        return redirect(url_for('orderData.order_list'))

    deleteOrder(orderId)
    flash(Messages.SUCCESS_DELETED, Messages.SUCCESS_CSS)
    return redirect(url_for('orderData.order_list'))


@orderData.route('/sub_order_list/')
@login_required
def sub_order_list():
    """件名小分類データ一覧の初期表示  GETのrequestを受付
    当処理はhtmlテンプレート及び画面用コンテンツを返します。
    """
    orderList = getOrderList(current_user.group_id)
    comboList = getOrderComBoList(orderList)
    cont = subOrderListCont(comboList)
    return render_template('order_data_management/sub-order-list.html', cont=cont)


@orderData.route('/list/getData/', methods = ['POST'])
@login_required
def sub_order_post_data():
    """件名小分類データ一覧表示用データ取得  POSTのrequestを受付

    一覧画面から選択されたカテゴリーのデータを取得し、json形式でデータを返します。

    :param orderCd: 選択された件名
    """
    try:
        orderCd = request.json['orderCd']
        models = getSubOrderList(current_user.group_id, orderCd)
        dataset = []
        for model in models:
            data = {}
            data["subOrderId"] = model.orderId
            data["clientName"] = model.clientName
            data["subOrderCd"] = model.subOrderCd
            data["subOrderValue"] = model.subOrderValue
            data["displayOrder"] = model.displayOrder
            data["isActive"] = model.isActive
            dataset.append(data)
    except:
        pass
    return jsonify(dataset)


@orderData.route('/sub_order_create/')
@login_required
def sub_order_create():
    """件名小分類データ作成処理
    
    件名小分類一覧画面から「新規作成」を押下後、GETのrequestを受付します。
    htmlテンプレート及び画面用コンテンツを返します。
    """
    clientList = getComItemList2('client_cd')
    orderList = getOrderList(current_user.group_id)
    form = SubOrderDataForm()
    form.clientCd.choices = [(i.item_cd, i.item_value) for i in clientList]
    form.orderCd.choices = [(i.orderCd, i.orderValue) for i in orderList]
    cont = detailsCont(form)
    return render_template('order_data_management/sub-order-details.html', cont=cont)


@orderData.route('/sub_order/<int:subOrderId>/edit/')
@login_required
def sub_order_edit(subOrderId):
    """件名小分類データ修正処理
    
    一覧画面からデータの「コード」を押下後、GETのrequestを受付します。
    htmlテンプレート及び画面用コンテンツを返します。

    :param subOrderId: 選択された件名小分類データのID
    """
    dto = getSubOrderDetails(subOrderId)
    if not dto:
        flash(Messages.WARNING_NOT_FOUND_ALREADY_UPDATED_DELETED, 
            Messages.WARNING_CSS)
        return redirect(url_for('orderData.sub_order_list'))

    clientList = getComItemList2('client_cd')
    orderList = getOrderList(current_user.group_id)
    form = SubOrderDataForm()
    form.clientCd.choices = [(i.item_cd, i.item_value) for i in clientList]
    form.orderCd.choices = [(i.orderCd, i.orderValue) for i in orderList]
    form.subOrderId.data = dto.sub_order_id
    form.clientCd.data = dto.client_cd
    form.orderCd.data = dto.order_cd
    form.subOrderCd.data = dto.sub_order_cd
    form.subOrderValue.data = dto.sub_order_value
    form.displayOrder.data = dto.display_order
    form.isActive.data = dto.is_active

    cont = detailsCont(form)
    return render_template('order_data_management/sub-order-details.html', cont=cont)


@orderData.route('/sub_order_details/save/', methods=['POST'])
@login_required
def sub_order_save():
    """件名小分類データ詳細画面登録処理

    formのデータをDBに保存します。
    処理終了後は件名小分類データ一覧画面へ遷移します。
    """
    clientList = getComItemList2('client_cd')
    orderList = getOrderList(current_user.group_id)
    form = SubOrderDataForm()
    form.clientCd.choices = [(i.item_cd, i.item_value) for i in clientList]
    form.orderCd.choices = [(i.orderCd, i.orderValue) for i in orderList]
    if form.validate_on_submit():
        if form.subOrderId.data:
            isUpdate = True
            dto = getSubOrderDetails(form.subOrderId.data)
            if dto:
                pass
            else:
                flash(Messages.WARNING_NOT_FOUND_ALREADY_UPDATED_DELETED, 
                    Messages.WARNING_CSS)
                return redirect(url_for('orderData.sub_order_list'))
        else:
            isUpdate = False
            result = checkUnique(
                form.clientCd.data,
                current_user.group_id,
                form.orderCd.data,
                form.subOrderCd.data
                )
            if result:
                pass
            else:
                flash(Messages.WARNING_UNIQUE_CONSTRAINT, Messages.WARNING_CSS)
                return redirect(url_for('orderData.sub_order_list'))
        data = form.data
        data['groupCd'] = current_user.group_id
        data['updateUser'] = current_user.user_id
        data['isActive'] = bool(form.isActive.data)

        insertUpdateSubOrder(data, isUpdate)
        if isUpdate:
            flash(Messages.SUCCESS_UPDATED, Messages.SUCCESS_CSS)
        else:
            flash(Messages.SUCCESS_INSERTED, Messages.SUCCESS_CSS)
        return redirect(url_for('orderData.sub_order_list'))

    for error in form.errors.values():
        flash(error[0],Messages.DANGER_CSS)

    cont = detailsCont(form)

    return render_template('order_data_management/sub-order-details.html', cont=cont)


@orderData.route('/sub_order_details/<int:subOrderId>/delete/')
@login_required
def sub_order_delete(subOrderId):
    """件名小分類データ詳細画面削除処理

    当該データを物理削除します。
    処理終了後は件名小分類データ一覧画面へ遷移します。

    :param subOrderId: 削除対象のIDです。
    """
    dto = getSubOrderDetails(subOrderId)
    if dto:
        pass
    else:
        flash(Messages.WARNING_NOT_FOUND_ALREADY_UPDATED_DELETED, 
            Messages.WARNING_CSS)
        return redirect(url_for('orderData.sub_order_list'))

    deleteSubOrder(subOrderId)
    flash(Messages.SUCCESS_DELETED, Messages.SUCCESS_CSS)
    return redirect(url_for('orderData.sub_order_list'))
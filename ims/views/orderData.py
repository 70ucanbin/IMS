from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for, session
from flask_login import login_required, current_user

from ims.common.ComboBoxUtil import getOrderList
from ims.common.Messages import Messages
from ims.contents.orderDataCont import OrderDataList as orderListCont
from ims.contents.orderDataCont import OrderDetails as orderDetailsCont
from ims.contents.orderDataCont import SubOrderDataList as subOrderListCont
from ims.contents.orderDataCont import SubOrderDetails as subOrderDetailsCont

from ims.form.orderDataForm import OrderDataForm
from ims.service.orderDataServ import getOrderList
from ims.service.orderDataServ import getOrderDetails
from ims.service.orderDataServ import checkUnique
from ims.service.orderDataServ import insertUpdateOrder
from ims.service.orderDataServ import deleteOrder

from ims.service.comServ import getComItemList2

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
    cont = orderDetailsCont(form)
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
                form.orderCd.data
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

    cont = orderDetailsCont(form)

    return render_template('order_data_management/order-details.html', cont=cont)
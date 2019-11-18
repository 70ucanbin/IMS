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


orderData = Blueprint('orderData', __name__)


@orderData.route('/list/')
@login_required
def order_data_list():
    """件名大分類データ一覧の初期表示  GETのrequestを受付
    当処理はhtmlテンプレート及び画面用コンテンツを返します。
    """
    data = getOrderList(current_user.group_id)
    cont = orderListCont(data)
    return render_template('order_data_management/order-list.html', cont=cont)



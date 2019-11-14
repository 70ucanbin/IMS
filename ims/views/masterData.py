import json

from datetime import datetime

from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for, session
from flask import Blueprint
from flask_login import login_required, current_user

from ims.common.Messages import Messages

from ims.common.ComboBoxUtil import getComCategoryList
from ims.contents.comCont import MasterDataList as listCont
from ims.contents.comCont import MasterDetails as detailsCont
from ims.service.comServ import insertUpdateMasterData as insertUpdateDto
from ims.service.comServ import getCategoryList as getDtoList

from ims.form.masterDateForm import MasterDataForm

masterData = Blueprint('masterData', __name__)


@masterData.route('/list/')
@login_required
def master_list():
    """マスタデータ一覧の初期表示  GETのrequestを受付
    当処理はhtmlテンプレート及び画面用コンテンツを返します。
    """
    categoryList = getDtoList('master_combo')
    comboList = getComCategoryList(categoryList)
    cont = listCont(comboList)
    category = session.get('pick_category')
    if category == 'undefined' or category == None:
        pass
    else:
        cont.dataCategory = category
    return render_template('master_data_management/master-list.html', cont=cont)


@masterData.route('/list/getData/', methods = ['POST'])
@login_required
def master_post_data():
    """マスタデータ一覧表示用データ取得  POSTのrequestを受付

    一覧画面から選択されたカテゴリーのデータを取得し、json形式でデータを返します。
    """
    try:
        category = request.json['category']
        models = getDtoList(category)
        dataset = []
        for model in models:
            data = {}
            data["itemCd"] = model.item_cd
            data["itemValue"] = model.item_value
            data["displayOrder"] = model.display_order
            data["isActive"] = model.is_active
            dataset.append(data)
    except:
        pass
    return jsonify(dataset)


@masterData.route('/create/')
@login_required
def master_create():
    """マスタデータ作成処理
    
    一覧画面から「新規作成」を押下後、GETのrequestを受付します。
    htmlテンプレート及び画面用コンテンツを返します。
    """
    categoryList = getDtoList('master_combo')
    form = MasterDataForm()
    form.itemCategory.choices = [(i.item_cd, i.item_value) for i in categoryList]
    cont = detailsCont(form)
    return render_template('master_data_management/master-details.html', cont=cont)


@masterData.route('/details/save/', methods=['POST'])
@login_required
def master_save():
    """マスタデータ詳細画面登録処理

    formのデータをDBに保存します。
    処理終了後はマスタデータ一覧画面へ遷移します。
    """
    categoryList = getDtoList('master_combo')
    form = MasterDataForm()
    form.itemCategory.choices = [(i.item_cd, i.item_value) for i in categoryList]
    if form.validate_on_submit():
        data = form.data
        data['updateUser'] = current_user.user_id
        # data['updateDate'] = datetime.now

        insertUpdateDto(data, False)
        
        return redirect(url_for('masterData.master_list'))
    for error in form.errors.values():
        flash(error[0],"list-group-item list-group-item-danger")

    cont = detailsCont(form)

    return render_template('master_data_management/master-details.html', cont=cont)







@masterData.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    pass

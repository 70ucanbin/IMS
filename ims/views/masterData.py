import json 

from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from flask import Blueprint
from flask_login import login_required, current_user

from ims.common.Messages import Messages

from ims.common.ComboBoxUtil import getComCategoryList
from ims.contents.comCont import MasterDataList as listCont
from ims.service.comServ import getCategoryList, getComUserList

from ims.form.masterDateForm import MasterDataForm

masterData = Blueprint('masterData', __name__)


@masterData.route('/list/')
@login_required
def master_list():
    """マスタデータ一覧の初期表示  GETのrequestを受付
    当処理はhtmlテンプレート及び画面用コンテンツを返します。
    """
 
    testList = getCategoryList('master_combo')
    categoryList = getComCategoryList(testList)
    cont = listCont(categoryList)

    return render_template('master_data_management/master-list.html', cont=cont)


@masterData.route('/list/getData/', methods = ['POST'])
@login_required
def master_post_data():
    """マスタデータ一覧表示用データ取得  POSTのrequestを受付

    一覧画面から選択されたカテゴリーのデータを取得し、json形式でデータを返します。
    """
    try:
        category = request.json['category']
        models = getCategoryList(category)
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

@masterData.route('/details/<string:userId>/edit')
@login_required
def user_edit(userId):
    """ユーザ一覧の初期表示  GETのrequestを受付
    当処理はhtmlテンプレート及び画面用コンテンツを返します。
    """
    pass

@masterData.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    pass

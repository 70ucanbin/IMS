from flask import Blueprint, flash, jsonify, request, redirect, render_template, session, url_for
from flask_login import login_required, current_user

from ims.common.ComboBoxUtil import getComCategoryList
from ims.common.Messages import Messages
from ims.common.RoleUtil import admin_required
from ims.contents.comCont import MasterDataList as listCont
from ims.contents.comCont import MasterDetails as detailsCont
from ims.form.masterDataForm import MasterDataForm
from ims.service.comServ import insertUpdateMasterData as insertUpdateDto
from ims.service.comServ import getComItemList as getDtoList
from ims.service.comServ import getComItem as getDto
from ims.service.comServ import deleteMasterData as deleteDto

masterData = Blueprint('masterData', __name__)


@masterData.route('/list/')
@admin_required
def master_list():
    """マスタデータ一覧の初期表示  GETのrequestを受付
    当処理はhtmlテンプレート及び画面用コンテンツを返します。
    """
    categoryList = getDtoList('master_combo')
    comboList = getComCategoryList(categoryList)
    cont = listCont(comboList)
    return render_template('master_data_management/master-list.html', cont=cont)


@masterData.route('/list/getData/', methods = ['POST'])
@admin_required
def master_post_data():
    """マスタデータ一覧表示用データ取得  POSTのrequestを受付

    一覧画面から選択されたカテゴリーのデータを取得し、json形式でデータを返します。

    :param category: 選択されたカテゴリー
    """
    try:
        category = request.json['category']
        models = getDtoList(category)
        dataset = []
        for model in models:
            data = {}
            data["itemId"] = model.item_id
            data["itemCd"] = model.item_cd
            data["itemValue"] = model.item_value
            data["displayOrder"] = model.display_order
            data["isActive"] = model.is_active
            dataset.append(data)
    except:
        pass
    return jsonify(dataset)


@masterData.route('/create/')
@admin_required
def master_create():
    """マスタデータ作成処理
    
    一覧画面から「新規作成」を押下後、GETのrequestを受付します。
    htmlテンプレート及び画面用コンテンツを返します。
    """
    categoryList = getDtoList('master_combo')
    comboList = getComCategoryList(categoryList)
    form = MasterDataForm()
    form.itemCategory.choices = [(i.key, i.value) for i in comboList]
    cont = detailsCont(form)
    return render_template('master_data_management/master-details.html', cont=cont)


@masterData.route('/<int:itemId>/edit/')
@admin_required
def master_edit(itemId):
    """マスタデータ修正処理
    
    一覧画面からデータの「コード」を押下後、GETのrequestを受付します。
    htmlテンプレート及び画面用コンテンツを返します。

    :param itemId: 対象データのID
    """
    dto = getDto(itemId)
    if not dto:
        flash(Messages.WARNING_NOT_FOUND_ALREADY_UPDATED_DELETED, 
            Messages.WARNING_CSS)
        return redirect(url_for('masterData.master_list'))

    categoryList = getDtoList('master_combo')
    form = MasterDataForm()
    form.itemCategory.choices = [(i.item_cd, i.item_value) for i in categoryList]
    form.itemId.data = dto.item_id
    form.itemCategory.data = dto.item_category
    form.itemCD.data = dto.item_cd
    form.itemValue.data = dto.item_value
    form.displayOrder.data = dto.display_order
    form.isActive.data = dto.is_active

    cont = detailsCont(form)
    return render_template('master_data_management/master-details.html', cont=cont)


@masterData.route('/details/save/', methods=['POST'])
@admin_required
def master_save():
    """マスタデータ詳細画面登録処理

    formのデータをDBに保存します。
    処理終了後はマスタデータ一覧画面へ遷移します。
    """
    categoryList = getDtoList('master_combo')
    comboList = getComCategoryList(categoryList)
    form = MasterDataForm()
    form.itemCategory.choices = [(i.key, i.value) for i in comboList]
    if form.validate_on_submit():
        if form.itemId.data:
            isUpdate = True
            dto = getDto(form.itemId.data)
            if dto:
                pass
            else:
                flash(Messages.WARNING_NOT_FOUND_ALREADY_UPDATED_DELETED, 
                    Messages.WARNING_CSS)
                return redirect(url_for('masterData.master_list'))
        else:
            isUpdate = False

        data = form.data
        data['updateUser'] = current_user.user_id
        data['isActive'] = bool(form.isActive.data)

        try:
            insertUpdateDto(data, isUpdate)
        except Exception:
            return redirect(url_for('masterData.master_list'))

        if isUpdate:
            flash(Messages.SUCCESS_UPDATED, Messages.SUCCESS_CSS)
        else:
            flash(Messages.SUCCESS_INSERTED, Messages.SUCCESS_CSS)
        return redirect(url_for('masterData.master_list'))

    for error in form.errors.values():
        flash(error[0],Messages.DANGER_CSS)

    cont = detailsCont(form)

    return render_template('master_data_management/master-details.html', cont=cont)


@masterData.route('/details/<int:itemId>/delete/')
@admin_required
def master_delete(itemId):
    """マスタデータ詳細画面削除処理

    当該データを物理削除します。
    処理終了後はマスタデータ一覧画面へ遷移します。

    :param itemId: 削除対象のIDです。
    """
    dto = getDto(itemId)
    if dto:
        pass
    else:
        flash(Messages.WARNING_NOT_FOUND_ALREADY_UPDATED_DELETED, 
            Messages.WARNING_CSS)
        return redirect(url_for('masterData.master_list'))

    deleteDto(itemId)
    flash(Messages.SUCCESS_DELETED, Messages.SUCCESS_CSS)
    return redirect(url_for('masterData.master_list'))
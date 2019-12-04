from flask import redirect, url_for, render_template, flash, session
from flask import Blueprint
from flask_login import login_required, current_user

from ims import bcrypt
from ims.common.Messages import Messages
from ims.common.RoleUtil import admin_required
from ims.service.comServ import getComUserList, getComUser, getComItemList, insertUpdateComUser
from ims.contents.userCont import UserListCont as listCont
from ims.contents.userCont import UserDetailsCont as detailsCont

from ims.form.userForm import UserForm

userManagement = Blueprint('userManagement', __name__)


@userManagement.route('/list/')
@admin_required
def user_list():
    """ユーザ一覧の初期表示  GETのrequestを受付
    当処理はhtmlテンプレート及び画面用コンテンツを返します。
    """
    userList = getComUserList(current_user.group_id)
    cont = listCont(userList)
    return render_template('user_management/user-list.html', cont=cont)

@userManagement.route('/details/create')
@admin_required
def user_create():
    """ユーザー作成処理

    一覧画面から「新規作成」を押下後、GETのrequestを受付します。
    htmlテンプレート及び画面用コンテンツを返します。
    """
    groupIdList = getComItemList('group_id')
    form = UserForm()
    
    form.groupId.choices = [(i.item_cd, i.item_value) for i in groupIdList]
    cont = detailsCont(form)
    return render_template('user_management/user-details.html', cont=cont)

@userManagement.route('/details/<string:userId>/edit')
@admin_required
def user_edit(userId):
    """ユーザー修正処理

    一覧画面から「月日」を押下後、GETのrequestを受付します。
    htmlテンプレート及び画面用コンテンツを返します。

    :param userId: 修正対象データのID
    """
    dto = getComUser(userId)
    if not dto:
        flash(Messages.WARNING_NOT_FOUND_ALREADY_UPDATED_DELETED, 
            Messages.WARNING_CSS)
        return redirect(url_for('userManagement.user_list'))

    groupIdList = getComItemList('group_id')
    form = UserForm()
    form.groupId.choices = [(i.item_cd, i.item_value) for i in groupIdList]

    form.userId.data = dto.user_id
    form.userName.data = dto.user_name
    form.groupId.data = dto.group_id
    form.role.data = dto.role
    form.email.data = dto.email

    cont = detailsCont(form)
    return render_template('user_management/user-details.html', cont=cont)

@userManagement.route('/details/save/', methods=['POST'])
@admin_required
def user_save():
    """ユーザー情報詳細画面登録処理

    formのデータをDBに保存します。
    処理終了後はマスタユーザー一覧画面へ遷移します。
    """
    groupIdList = getComItemList('group_id')
    form = UserForm()
    form.groupId.choices = [(i.item_cd, i.item_value) for i in groupIdList]
    if form.validate_on_submit():
        data = form.data
        data['password'] = bcrypt.generate_password_hash(form.password.data).decode(encoding='utf-8')
        isUpdate = False
        dto = getComUser(data['userId'])
        if dto:
            isUpdate = True
        insertUpdateComUser(data, isUpdate)
        if isUpdate:
            flash(Messages.SUCCESS_UPDATED, Messages.SUCCESS_CSS)
        else:
            flash(Messages.SUCCESS_INSERTED, Messages.SUCCESS_CSS)
        return redirect(url_for('userManagement.user_list'))
    for error in form.errors.values():
        flash(error[0], Messages.DANGER_CSS)
    cont = detailsCont(form)
    return render_template('user_management/user-details.html', cont=cont)


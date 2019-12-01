from flask import redirect, url_for, render_template, flash, session
from flask import Blueprint
from flask_login import login_required, current_user

from ims.common.Messages import Messages

from ims import bcrypt
from ims.service.comServ import getComUserList, getComUser, insertUpdateComUser

from ims.form.userForm import UserForm

userManagement = Blueprint('userManagement', __name__)


@userManagement.route('/list/')
@login_required
def user_list():
    """ユーザ一覧の初期表示  GETのrequestを受付
    当処理はhtmlテンプレート及び画面用コンテンツを返します。
    """
    if current_user.is_manager:
        userList = getComUserList(current_user.group_id)
        return render_template('user_management/user-list.html', dataSet=userList)
    else:
        return redirect(url_for('home.index'))

@userManagement.route('/details/<string:userId>/edit')
@login_required
def user_edit(userId):
    """ユーザ一覧の初期表示  GETのrequestを受付
    当処理はhtmlテンプレート及び画面用コンテンツを返します。
    """
    form = UserForm()
    return render_template('user_management/user-details.html', form=form)

@userManagement.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    form = UserForm()
    if form.validate_on_submit():
        dto = form.data
        dto['password'] = bcrypt.generate_password_hash(form.password.data).decode(encoding='utf-8')
        insertUpdateComUser(dto)
    return render_template('user_management/user-details.html', form=form)


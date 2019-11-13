from flask import redirect, url_for, render_template, flash, session
from flask import Blueprint
from flask_login import login_required, current_user

from ims.common.Messages import Messages

from ims import bcrypt
from ims.common.ComboBoxUtil import getComCategoryList
from ims.contents.comCont import MasterDataList as listCont
from ims.service.comServ import selectComItemList2, getComUserList, getComUser, insertUpdateComUser

from ims.form.masterDateForm import MasterDataForm

masterData = Blueprint('masterData', __name__)


@masterData.route('/list/')
@login_required
def master_list():
    """マスタデータ一覧の初期表示  GETのrequestを受付
    当処理はhtmlテンプレート及び画面用コンテンツを返します。
    """
    testList = selectComItemList2('99')
    cont = listCont(testList)
    if current_user.is_manager:
        userList = getComUserList(current_user.group_id)
        return render_template('master_data_management/master-list.html', dataSet=userList)
    else:
        return redirect(url_for('home.index'))

@masterData.route('/details/<string:userId>/edit')
@login_required
def user_edit(userId):
    """ユーザ一覧の初期表示  GETのrequestを受付
    当処理はhtmlテンプレート及び画面用コンテンツを返します。
    """
    form = MasterDataForm()
    user = getComUser(userId)
    return render_template('master_data_management/master-register.html', form=form)

@masterData.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    form = MasterDataForm()
    if form.validate_on_submit():
        dto = form.data
        dto['password'] = bcrypt.generate_password_hash(form.password.data).decode(encoding='utf-8')
        insertUpdateComUser(dto)
    return render_template('master_data_management/master-register.html', form=form)

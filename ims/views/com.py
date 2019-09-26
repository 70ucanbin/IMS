from flask import redirect, url_for, render_template, flash
from flask import Blueprint
from flask_login import login_user, logout_user, current_user

from ims import bcrypt
from ims.service.comServ import getComUser, insertUpdateComUser

from ims.form.userForm import UserForm

com = Blueprint('com', __name__)


@com.route('/register', methods=['GET', 'POST'])
def register():
    form = UserForm()
    if form.validate_on_submit():
        dto = form.data
        dto['password'] = bcrypt.generate_password_hash(form.password.data).decode(encoding='utf-8')
        insertUpdateComUser(dto)
    return render_template('register.html', form=form)


@com.route('/login', methods=['GET', 'POST'])
def login():
    """ユーザのログイン処理  GET,POSTの両方を受付
    ログインされてない場合はログイン画面を表示します。
    """
    if current_user.is_authenticated:
        return redirect(url_for('home.index'))
    form = UserForm()
    if form.validate_on_submit():
        user = getComUser(form.userId.data)
        password = form.password.data
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('home.index'))
        flash('usernameまたはPasswordが異なります',"list-group-item list-group-item-danger")
    return render_template('login.html',form=form)

# ログアウト処理
@com.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('com.login'))

@com.route('/error')
def system_error():

    "ここにlog出力・エラーメッセージ処理記述"

    

    return render_template('error.html')
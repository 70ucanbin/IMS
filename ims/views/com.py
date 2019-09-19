from functools import wraps

from flask import request, redirect, url_for, render_template, flash, session
from flask import Blueprint
from flask_login import login_user, login_required, current_user

from ims import bcrypt
from ims.service.comServ import getComUser, insertUpdateComUser

from ims.form.userForm import UserForm

com = Blueprint('com', __name__)

# デコレーター
# session保持の判定を実施し、sessionが存在しなければ、ログイン画面へ遷移する、元関数の実行をしない
# def login_required(view):
#     @wraps(view)
#     def inner(*args, **kwargs):
#         if not session.get('logged_in'):
#             return redirect(url_for('com.login'))
#         return view(*args, **kwargs)
#     return inner

# ログイン処理

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
    if current_user.is_authenticated:
        return redirect(url_for('home.index'))
    form = UserForm()
    # if request.method == 'POST':
    if form.validate_on_submit():
        user = getComUser(form.userId.data)
        password = form.password.data
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            session['logged_in'] = True
            return redirect(url_for('home.index'))
        flash('usernameまたはPasswordが異なります',"list-group-item list-group-item-danger")

    # if request.method == 'POST':
    #     if request.form['userId'] != 'USERNAME':
    #         flash('ユーザ名が異なります')
    #     elif request.form['password'] != 'PASSWORD':
    #         flash('パスワードが異なります')
    #     else:
    #         session['logged_in'] = True
    #         # flash('ログインしました')
    #         return redirect(url_for('home.index'))
    return render_template('login.html',form=form)
    # print(form.errors)
    # return render_template('login.html', form=form)

# ログアウト処理
@com.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('home.index'))

@com.route('/error')
def system_error():

    "ここにlog出力・エラーメッセージ処理記述"

    

    return render_template('error.html')
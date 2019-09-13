from functools import wraps

from flask import request, redirect, url_for, render_template, flash, session
from flask import Blueprint
from flask_bcrypt import Bcrypt

from ims.form.userForm import UserForm

com = Blueprint('com', __name__)

# デコレーター
# session保持の判定を実施し、sessionが存在しなければ、ログイン画面へ遷移する、元関数の実行をしない
def login_required(view):
    @wraps(view)
    def inner(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('com.login'))
        return view(*args, **kwargs)
    return inner

# ログイン処理
@com.route('/login', methods=['GET', 'POST'])
def login():
    form = UserForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            session['logged_in'] = True
            return redirect(url_for('home.index'))
        # if request.form['username'] != 'USERNAME':
        #     flash('usernameまたはPasswordが異なります',"list-group-item list-group-item-danger")
        # elif request.form['password'] != 'PASSWORD':
        #     flash('パスワードが異なります')
        # else:
        #     session['logged_in'] = True
        #     # flash('ログインしました')
        #     return redirect(url_for('home.index'))
        print(form.errors)
        flash('usernameまたはPasswordが異なります',"list-group-item list-group-item-danger")
    return render_template('login.html', form=form)

# ログアウト処理
@com.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('home.index'))

@com.route('/error')
def system_error():

    "ここにlog出力・エラーメッセージ処理記述"

    

    return render_template('error.html')
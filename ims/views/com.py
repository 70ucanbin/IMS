from flask import request, redirect, url_for, render_template, flash, session
from flask import Blueprint
from functools import wraps

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
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'USERNAME':
            flash('ユーザ名が異なります')
        elif request.form['password'] != 'PASSWORD':
            flash('パスワードが異なります')
        else:
            session['logged_in'] = True
            flash('ログインしました')
            return redirect(url_for('home.index'))
    return render_template('login.html')

# ログアウト処理
@com.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('ログアウトしました')
    return redirect(url_for('home.index'))

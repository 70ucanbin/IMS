from flask import request, redirect, url_for, render_template, flash, session, Blueprint
from flask_login import login_required

home = Blueprint('home', __name__)

@home.route('/')
@login_required
def index():
    if not session.get('logged_in'):
        return redirect(url_for('com.login'))
    return render_template('index.html')


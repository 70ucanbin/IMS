from flask import request, redirect, url_for, render_template, flash, session, Blueprint
from ims.views.com import login_required

home = Blueprint('home', __name__)

@home.route('/')
@login_required
def index():
    activeHome = 'cwl'
    if not session.get('logged_in'):
        return redirect(url_for('com.login'))
    return render_template('index.html', activeHome=activeHome)


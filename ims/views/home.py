from flask import request, redirect, url_for, render_template, flash, session, Blueprint
from flask_login import login_required

home = Blueprint('home', __name__)

@home.route('/')
@login_required
def index():
    return render_template('index.html')


from flask import render_template, Blueprint
from flask_login import login_required

home = Blueprint('home', __name__)

@home.route('/')
@login_required
def index():
    return render_template('index.html')
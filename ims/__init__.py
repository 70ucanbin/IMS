from datetime import timedelta

from flask import Flask, redirect, url_for, render_template, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

from config import AppConfig as __Config


app = Flask(__name__)
app.config.from_object(__Config)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login = LoginManager(app)
login.login_view = 'com.login'
login.login_message = 'ログインしてから操作を続けてください'
login.login_message_category = 'list-group-item list-group-item-danger'


@app.before_request
def before_request():
    session.permanent = False
    app.permanent_session_lifetime = timedelta(minutes=10)

from ims.views import com, home, clientWork, monthlyReport, travelExpenses, orderData, userManagement, masterData

app.register_blueprint(com.com)
app.register_blueprint(home.home)
app.register_blueprint(clientWork.clientWork, url_prefix='/client_work')
app.register_blueprint(monthlyReport.monthlyReport, url_prefix='/monthly_report')
app.register_blueprint(travelExpenses.travelExpenses, url_prefix='/travel_expenses')
app.register_blueprint(orderData.orderData, url_prefix='/order_data')
app.register_blueprint(masterData.masterData, url_prefix='/master_data')
app.register_blueprint(userManagement.userManagement, url_prefix='/user_management')


@app.errorhandler(403)
def forbidden_route(error):
    return redirect(url_for('com.forbidden_error'))

@app.errorhandler(404)
def not_found_route(error):
    return redirect(url_for('com.not_found_error'))

@app.errorhandler(500)
def system_exception(error):
    return redirect(url_for('com.system_error'))

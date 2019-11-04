from flask import Flask, redirect, url_for, render_template
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
# login_manager = flask_login.LoginManager()
# login_manager.init_app(app)


from ims.views import com, home, clientWork, monthlyReport, travelExpenses, testapi ,userManagement, masterDataManagement

app.register_blueprint(com.com)
app.register_blueprint(home.home)
app.register_blueprint(clientWork.clientWork, url_prefix='/client_work')
app.register_blueprint(monthlyReport.monthlyReport, url_prefix='/monthly_report')
app.register_blueprint(travelExpenses.travelExpenses, url_prefix='/travel_expenses')
app.register_blueprint(testapi.api, url_prefix='/api')
app.register_blueprint(userManagement.userManagement, url_prefix='/userManagement')
app.register_blueprint(masterDataManagement.masterDataManagement, url_prefix='/masterDataManagement')


# from ims.views import clientWork

@app.errorhandler(404)
def non_existant_route(error):
    return redirect(url_for('com.login'))

@app.errorhandler(500)
def system_exception(error):
    return redirect(url_for('com.system_error'))

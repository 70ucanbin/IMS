from flask import Flask, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

from ims.views import com, home, clientWork, monthlyReport, travelExpenses, testapi

app.register_blueprint(com.com)
app.register_blueprint(home.home)
app.register_blueprint(clientWork.clientWork, url_prefix='/client_work')
app.register_blueprint(monthlyReport.monthlyReport, url_prefix='/monthly_report')
app.register_blueprint(travelExpenses.travelExpenses)
app.register_blueprint(testapi.api, url_prefix='/api')

# from ims.views import clientWork

@app.errorhandler(404)
def non_existant_route(error):
    return redirect(url_for('com.login'))

@app.errorhandler(500)
def system_exception(error):
    return redirect(url_for('com.system_error'))

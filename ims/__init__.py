from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from ims.views import com, home, clientWork

app = Flask(__name__)
app.config.from_object('config')
app.register_blueprint(com.com)
app.register_blueprint(home.home)
app.register_blueprint(clientWork.clientWork)

@app.errorhandler(404)
def non_existant_route(error):
    return redirect(url_for('com.login'))


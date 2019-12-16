from flask import Flask
import click
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.schema import Sequence, CreateSequence
from flask_bcrypt import Bcrypt
from config import AppConfig as __Config
from datetime import datetime

app = Flask(__name__)
app.config.from_object(__Config)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

class User(db.Model):
    __tablename__ = 'com_user'
    user_id = db.Column(db.String(20), primary_key=True)
    group_id = db.Column(db.String(20))
    role = db.Column(db.SMALLINT, nullable=False)
    user_name = db.Column(db.String(20))
    password = db.Column(db.String(150))
    email = db.Column(db.String(50))
    is_active = db.Column(db.Boolean, server_default=u'True')
    update_user = db.Column(db.String(20))
    update_date = db.Column(db.DateTime, default=datetime.now)

class ComItem(db.Model):
    __tablename__ = 'com_item'
    item_id = db.Column(db.Integer, db.Sequence('com_item_seq'), unique=True, nullable=False)
    item_category = db.Column(db.String(20), primary_key=True)
    item_cd = db.Column(db.String(20), primary_key=True)
    item_value = db.Column(db.String(100))
    display_order = db.Column(db.Integer)
    is_active = db.Column(db.Boolean, server_default=u'True')
    update_user = db.Column(db.String(20))
    update_date = db.Column(db.DateTime, default=datetime.now)

class TraClientWork(db.Model):
    __tablename__ = 'tra_client_work'
    client_work_id = db.Column(db.Integer, db.Sequence('tra_client_work_seq'), primary_key=True)
    user_id = db.Column(db.String(20), primary_key=True)
    work_year = db.Column(db.SMALLINT , primary_key=True)
    work_month = db.Column(db.SMALLINT , primary_key=True)
    work_day = db.Column(db.SMALLINT)
    rest_flg = db.Column(db.SMALLINT)
    order_cd = db.Column(db.String(20))
    task_cd = db.Column(db.String(20))
    sub_order_cd = db.Column(db.String(20))
    work_time = db.Column(db.Time)
    note = db.Column(db.String(200))

class TraMonthlyReport(db.Model):
    __tablename__ = 'tra_monthly_report'
    user_id = db.Column(db.String(20), primary_key=True)
    work_year = db.Column(db.Integer, primary_key=True)
    work_month = db.Column(db.Integer, primary_key=True)
    work_day = db.Column(db.Integer, primary_key=True)
    rest_flg = db.Column(db.Integer)
    work_details = db.Column(db.String(100))
    start_work_time = db.Column(db.DateTime)
    end_work_time = db.Column(db.DateTime)
    normal_working_hours = db.Column(db.Numeric(4,2))
    overtime_hours = db.Column(db.Numeric(4,2))
    holiday_work_hours = db.Column(db.Numeric(4,2))
    note = db.Column(db.String(200))

class TraTravelExpenses(db.Model):
    __tablename__ = 'tra_travel_expenses'
    travel_expenses_id = db.Column(db.Integer, db.Sequence('tra_travel_expenses_seq'), primary_key=True)
    user_id = db.Column(db.String(20), nullable=False)
    entry_year = db.Column(db.Integer, nullable=False)
    entry_month = db.Column(db.Integer, nullable=False)
    expense_date = db.Column(db.String(30))
    expense_item = db.Column(db.String(50))
    route = db.Column(db.String(50))
    transit = db.Column(db.String(50))
    payment = db.Column(db.Integer)
    file_name = db.Column(db.String(100))
    note = db.Column(db.String(200))

class TraOrder(db.Model):
    __tablename__ = 'tra_order'
    order_id = db.Column(db.Integer, db.Sequence('tra_order_seq'), unique=True, nullable=False)
    client_cd = db.Column(db.String(20), primary_key=True)
    group_id = db.Column(db.String(20), primary_key=True)
    order_cd = db.Column(db.String(20), primary_key=True)
    order_value = db.Column(db.String(100))
    display_order = db.Column(db.Integer)
    is_active = db.Column(db.Boolean, server_default=u'True')
    update_user = db.Column(db.String(20))
    update_date = db.Column(db.DateTime, default=datetime.now)

class TraSubOrder(db.Model):
    __tablename__ = 'tra_sub_order'
    sub_order_id = db.Column(db.Integer, db.Sequence('tra_sub_order_seq'), unique=True, nullable=False)
    client_cd = db.Column(db.String(20), primary_key=True)
    group_id = db.Column(db.String(20), primary_key=True)
    order_cd = db.Column(db.String(20), primary_key=True)
    sub_order_cd = db.Column(db.String(20), primary_key=True)
    sub_order_value = db.Column(db.String(100))
    display_order = db.Column(db.Integer)
    is_active = db.Column(db.Boolean, server_default=u'True')
    update_user = db.Column(db.String(20))
    update_date = db.Column(db.DateTime, default=datetime.now)

@click.command(name='setup')
@with_appcontext
def setup():
    db.drop_all()
    db.create_all()

    user = User()
    user.user_id = 'admin'
    user.user_name = 'Admin'
    user.password = bcrypt.generate_password_hash('password').decode(encoding='utf-8')
    user.group_id = 'manager'
    user.role = 3
    user.email = 'admin@test.com'
    user.update_user = 'admin'
    db.session.add(user)

    master_combo1 = ComItem()
    master_combo1.item_category = 'master_combo'
    master_combo1.item_cd = 'group_id'
    master_combo1.item_value = '所属部署'
    master_combo1.display_order = 1
    master_combo1.update_user = 'Admin'
    db.session.add(master_combo1)

    master_combo2 = ComItem()
    master_combo2.item_category = 'master_combo'
    master_combo2.item_cd = 'client_cd'
    master_combo2.item_value = '客先'
    master_combo2.display_order = 2
    master_combo2.update_user = 'Admin'
    db.session.add(master_combo2)

    client_cd = ComItem()
    client_cd.item_category = 'client_cd'
    client_cd.item_cd = '999999999'
    client_cd.item_value = '自社作業・応援'
    client_cd.display_order = 1
    client_cd.update_user = 'Admin'
    db.session.add(client_cd)

    group_id = ComItem()
    group_id.item_category = 'group_id'
    group_id.item_cd = 'manager'
    group_id.item_value = '管理者グループ'
    group_id.display_order = 1
    group_id.update_user = 'Admin'
    db.session.add(group_id)

    order = TraOrder()
    order.client_cd = '999999999'
    order.group_id = 'manager'
    order.order_cd = '999999999'
    order.order_value = '自社作業'
    order.display_order = 1
    order.update_user = 'Admin'
    db.session.add(order)

    db.session.commit()

app.cli.add_command(setup)
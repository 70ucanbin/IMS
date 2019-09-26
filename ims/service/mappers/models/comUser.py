from datetime import datetime
from flask_login import UserMixin
from ims import db, login

@login.user_loader
def load_user(user_id):
    try:
        return User.query.get(user_id)
    except:
        return None


class User(db.Model, UserMixin):
    __tablename__ = 'com_user'
    user_id = db.Column(db.String(20), primary_key=True)
    group_id = db.Column(db.String(20))
    is_manager = db.Column(db.Integer)
    user_name = db.Column(db.String(20))
    password = db.Column(db.String(50))
    email = db.Column(db.String(50))
    delete_flg = db.Column(db.Integer)
    update_user = db.Column(db.String(20))
    update_date = db.Column(db.DateTime)

    def __init__(self, user_id=None, group_id=None, user_name=None,\
            password=None, email=None, delete_flg=0, update_user=None):
        self.user_id = user_id
        self.group_id = group_id
        self.user_name = user_name
        self.password = password
        self.email = email
        self.delete_flg = delete_flg
        self.update_user = update_user
        self.update_date = datetime.utcnow()

    def is_active(self):
        return True

    def get_id(self):
        return (self.user_id)

    def __repr__(self):
        return '<User user_name:{}>'.format(self.user_name)
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
    role = db.Column(db.Integer, nullable=False)
    user_name = db.Column(db.String(20))
    password = db.Column(db.String(150))
    email = db.Column(db.String(50))
    is_active = db.Column(db.Boolean, default=True)
    update_user = db.Column(db.String(20))
    update_date = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, user_id=None, group_id=None, user_name=None):
        self.user_id = user_id
        self.group_id = group_id
        self.user_name = user_name

    def get_id(self):
        return (self.user_id)

    def __repr__(self):
        return '<User user_name:{}>'.format(self.user_name)
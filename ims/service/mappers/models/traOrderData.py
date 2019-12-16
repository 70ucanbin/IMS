from datetime import datetime

from ims import db


class TraOrder(db.Model):
    __tablename__ = 'tra_order'
    order_id = db.Column(db.Integer, db.Sequence('tra_order_seq'), unique=True, nullable=False)
    client_cd = db.Column(db.String(20), primary_key=True)
    group_id = db.Column(db.String(20), primary_key=True)
    order_cd = db.Column(db.String(20), primary_key=True)
    order_value = db.Column(db.String(100))
    display_order = db.Column(db.Integer)
    is_active = db.Column(db.Boolean, default=True)
    update_user = db.Column(db.String(20))
    update_date = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, client_cd=None, group_id=None, order_cd=None):
        self.client_cd = client_cd
        self.group_id = group_id
        self.order_cd = order_cd

    def __repr__(self):
        return '<TraOrder cd:{} value:{}>'.format(self.order_cd, self.order_value)


class TraSubOrder(db.Model):
    __tablename__ = 'tra_sub_order'
    sub_order_id = db.Column(db.Integer, db.Sequence('tra_sub_order_seq'), unique=True, nullable=False)
    client_cd = db.Column(db.String(20), primary_key=True)
    group_id = db.Column(db.String(20), primary_key=True)
    order_cd = db.Column(db.String(20), primary_key=True)
    sub_order_cd = db.Column(db.String(20), primary_key=True)
    sub_order_value = db.Column(db.String(100))
    display_order = db.Column(db.Integer)
    is_active = db.Column(db.Boolean, default=True)
    update_user = db.Column(db.String(20))
    update_date = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, client_cd=None, group_id=None, order_cd=None, sub_order_cd=None):
        self.client_cd = client_cd
        self.group_id = group_id
        self.order_cd = order_cd
        self.sub_order_cd = sub_order_cd

    def __repr__(self):
        return '<TraSubOrder cd:{} value:{}>'.format(self.sub_order_cd, self.sub_order_value)
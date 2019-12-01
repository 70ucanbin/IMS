from datetime import datetime

from ims import db

class ComItem(db.Model):
    __tablename__ = 'com_item'
    item_id = db.Column(db.Integer, db.Sequence('com_item_seq'), primary_key=True)
    item_category = db.Column(db.String(2), primary_key=True)
    item_cd = db.Column(db.String(20), primary_key=True)
    item_value = db.Column(db.String(100))
    display_order = db.Column(db.Integer)
    is_active = db.Column(db.Boolean, default=True)
    update_user = db.Column(db.String(20))
    update_date = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, item_category=None, item_cd=None, item_value=None):
        self.item_category = item_category
        self.item_cd = item_cd
        self.item_value = item_value
        self.display_order = 0


    def __repr__(self):
        return '<ComItem key:{} value:{}>'.format(self.item_cd, self.item_value)
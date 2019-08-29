from ims import db

class ComItem(db.Model):
    __tablename__ = 'com_item'
    item_category = db.Column(db.String(2), primary_key=True)
    item_key = db.Column(db.String(20), primary_key=True)
    item_value = db.Column(db.String(100))
    display_order = db.Column(db.Integer)

    def __init__(self, item_category=None, item_key=None, item_value=None, display_order=None):
        self.item_category = item_category
        self.item_key = item_key
        self.item_value = item_value
        self.display_order = display_order

    def __repr__(self):
        return '<ComItem key:{} value:{}>'.format(self.item_key, self.item_value)
from ims import db

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

    def __init__(self, travel_expenses_id=None):
        self.travel_expenses_id = travel_expenses_id

    def __repr__(self):
        return '<model id:{}>'.format(self.travel_expenses_id)
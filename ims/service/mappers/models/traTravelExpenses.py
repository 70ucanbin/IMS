from ims import db

class TraTravelExpenses(db.Model):
    __tablename__ = 'tra_travel_expenses'
    travel_expenses_id = db.Column(db.Integer, db.Sequence('tra_travel_expenses_seq'), primary_key=True)
    user_id = db.Column(db.String(20))
    entry_year = db.Column(db.Integer)
    entry_month = db.Column(db.Integer)
    expense_date = db.Column(db.String(30))
    expense_item = db.Column(db.String(50))
    route = db.Column(db.String(50))
    transit = db.Column(db.String(50))
    payment = db.Column(db.Integer)
    file_name = db.Column(db.String(100))
    note = db.Column(db.String(200))

    def __init__(self, travel_expenses_id=None, user_id=None, \
            work_year=None, work_month=None, expense_date=None, \
            expense_item=None, route=None, transit=None, \
            payment=None, file_name=None, note=None):
        self.travel_expenses_id = travel_expenses_id
        self.user_id = user_id
        self.work_year = work_year
        self.work_month = work_month
        self.expense_date = expense_date
        self.expense_item = expense_item
        self.route = route
        self.payment = payment
        self.file_name = file_name
        self.note = note

    def __repr__(self):
        return '<Entry travel_expenses_id:{}>'.format(self.travel_expenses_id)
from ims import db

class TraTravelExpenses(db.Model):
    __tablename__ = 'tra_travel_expenses'
    travel_expenses_id = db.Column(db.String(20), primary_key=True)
    employee_id = db.Column(db.String(20))
    work_year = db.Column(db.Integer)
    work_month = db.Column(db.Integer)
    expense_item = db.Column(db.String(50))
    route = db.Column(db.String(50))
    transit = db.Column(db.String(50))
    payment = db.Column(db.Integer))
    attached_file_id = db.Column(db.String(20))
    note = db.Column(db.String(200))

    def __init__((self, travel_expenses_id=None, employee_id=None, work_year=None, work_month=None, expense_item=None,
            route=None, transit=None, payment=None, attached_file_id=None, note=None)):
        self.travel_expenses_id = employee_id
        self.employee_id = work_year
        self.work_year = work_month
        self.work_month = work_day
        self.expense_item = work_details
        self.route = start_work_time
        self.payment = end_work_time
        self.normal_working_hours = normal_working_hours
        self.attached_file_id = overtime_hours
        self.note = note

    def __repr__(self):
        return '<Entry travel_expenses_id:{}>'.format(self.travel_expenses_id)
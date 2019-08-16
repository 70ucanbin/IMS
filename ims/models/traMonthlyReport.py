from ims import db

class TraMonthlyReport(db.Model):
    __tablename__ = 'tra_monthly_report'
    employee_id = db.Column(db.String(20), primary_key=True)
    work_year = db.Column(db.Integer, primary_key=True)
    work_month = db.Column(db.Integer, primary_key=True)
    work_day = db.Column(db.Integer, primary_key=True)
    work_details = db.Column(db.String(100))
    start_work_hours = db.Column(db.Integer)
    start_work_minutes = db.Column(db.Integer)
    end_work_hours = db.Column(db.Integer)
    end_work_minutes = db.Column(db.Integer)
    normal_working_hours = db.Column(db.Numeric(3.1))
    overtime_hours = db.Column(db.Numeric(3.1))
    holiday_work_hours = db.Column(db.Numeric(3.1))
    note = db.Column(db.String(200))

    def __init__(self, employee_id=None, work_year=None, work_month=None, \
            work_day=None, work_details=None, start_work_hours=None,  \
            start_work_minutes=None, end_work_hours=None,  end_work_minutes=None, \
            normal_working_hours=None, overtime_hours=None, holiday_work_hours=None, \
            note=None):
        self.employee_id = employee_id
        self.work_year = work_year
        self.work_month = work_month
        self.work_day = work_day
        self.work_details = work_details
        self.start_work_hours = start_work_hours
        self.start_work_minutes = start_work_minutes
        self.end_work_hours = end_work_hours
        self.end_work_minutes = end_work_minutes
        self.normal_working_hours = normal_working_hours
        self.overtime_hours = overtime_hours
        self.holiday_work_hours = holiday_work_hours
        self.note = note

    def __repr__(self):
        return '<TraMonthlyReport employee_id:{} work_year:{} work_month:{} work_day:{}>'.format(self.employee_id, self.work_year, self.work_month, self.work_day)
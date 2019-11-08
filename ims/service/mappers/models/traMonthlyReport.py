from ims import db

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
    normal_working_hours = db.Column(db.Numeric(4.2))
    overtime_hours = db.Column(db.Numeric(4.2))
    holiday_work_hours = db.Column(db.Numeric(4.2))
    note = db.Column(db.String(200))

    def __init__(
            self, user_id=None, work_year=None, work_month=None, 
            work_day=None, work_details=None,
            start_work_time=None, end_work_time=None, 
            normal_working_hours=None, overtime_hours=None, holiday_work_hours=None, 
            note=None):
        self.user_id = user_id
        self.work_year = work_year
        self.work_month = work_month
        self.work_day = work_day
        self.work_details = work_details
        self.start_work_time = start_work_time
        self.end_work_time = end_work_time
        self.normal_working_hours = normal_working_hours
        self.overtime_hours = overtime_hours
        self.holiday_work_hours = holiday_work_hours
        self.note = note

    def __repr__(self):
        return '<TraMonthlyReport user_id:{} work_year:{} work_month:{} work_day:{}>'.format(
            self.user_id, 
            self.work_year, 
            self.work_month, 
            self.work_day
        )
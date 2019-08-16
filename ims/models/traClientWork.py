from ims import db

class TraClientWork(db.Model):
    __tablename__ = 'tra_client_work'
    employee_id = db.Column(db.String(20), primary_key=True)
    work_year = db.Column(db.Integer, primary_key=True)
    work_month = db.Column(db.Integer, primary_key=True)
    work_day = db.Column(db.Integer)
    order_cd = db.Column(db.String(20))
    task_cd = db.Column(db.String(20))
    sub_order_cd = db.Column(db.String(20))
    hours_of_work = db.Column(db.Integer)
    minutes_of_work = db.Column(db.Integer)
    note = db.Column(db.String(200))

    def __init__(self, employee_id=None, work_year=None, work_month=None, work_day=None, order_cd=None, task_cd=None, sub_order_cd=None, hours_of_work=None, minutes_of_work=None, note=None):
        self.employee_id = employee_id
        self.work_year = work_year
        self.work_month = work_month
        self.work_day = work_day
        self.order_cd = order_cd
        self.task_cd = task_cd
        self.sub_order_cd = sub_order_cd
        self.hours_of_work = hours_of_work
        self.minutes_of_work = minutes_of_work
        self.note = note

    def __repr__(self):
        return '<Entry employee_id:{} work_year:{} work_month:{} work_day:{}>'.format(self.employee_id, self.work_year, self.work_month, self.work_day)
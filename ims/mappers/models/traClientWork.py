from sqlalchemy import DateTime
from ims import db

class TraClientWork(db.Model):
    __tablename__ = 'tra_client_work'
    client_work_id = db.Column(db.Integer, db.Sequence('tra_client_work_seq'), primary_key=True)
    employee_id = db.Column(db.String(20), primary_key=True)
    work_year = db.Column(db.Integer, primary_key=True)
    work_month = db.Column(db.Integer, primary_key=True)
    work_day = db.Column(db.Integer)
    order_cd = db.Column(db.String(20))
    task_cd = db.Column(db.String(20))
    sub_order_cd = db.Column(db.String(20))
    work_time = db.Column(db.DateTime)
    note = db.Column(db.String(200))

    def __init__(self, employee_id=None, work_year=None, work_month=None, work_day=None, order_cd=None, task_cd=None, sub_order_cd=None, work_time=None, note=None):
        self.employee_id = employee_id
        self.work_year = work_year
        self.work_month = work_month
        self.work_day = work_day
        self.order_cd = order_cd
        self.task_cd = task_cd
        self.sub_order_cd = sub_order_cd
        self.work_time = work_time
        self.note = note

    def __repr__(self):
        return '<Entry employee_id:{} work_year:{} work_month:{} work_day:{}>'.format(self.employee_id, self.work_year, self.work_month, self.work_day)

# class workTime(db.Model):
#     workTime = db.Column(db.String(5))
#     def __init__(self, employee_id=None, work_year=None, work_month=None, work_day=None):
#         self.workTime = 
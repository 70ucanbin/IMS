from ims import db

class TraClientWork(db.Model):
    __tablename__ = 'tra_client_work'
    client_work_id = db.Column(db.Integer, db.Sequence('tra_client_work_seq'), unique=True, nullable=False)
    user_id = db.Column(db.String(20), primary_key=True)
    work_year = db.Column(db.SMALLINT , primary_key=True)
    work_month = db.Column(db.SMALLINT , primary_key=True)
    work_day = db.Column(db.SMALLINT )
    rest_flg = db.Column(db.SMALLINT , default=0)
    order_cd = db.Column(db.String(20))
    task_cd = db.Column(db.String(20))
    sub_order_cd = db.Column(db.String(20))
    work_time = db.Column(db.Time)
    note = db.Column(db.String(200))

    def __init__(self, user_id=None, work_year=None, work_month=None, work_day=None):
        self.user_id = user_id
        self.work_year = work_year
        self.work_month = work_month
        self.work_day = work_day

    def __repr__(self):
        return '<Entry client_work_id:{}>'.format(self.client_work_id)
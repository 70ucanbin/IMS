from ims import db

class ComEmployee(db.Model):
    __tablename__ = 'com_employee'
    employee_id = db.Column(db.String(20), primary_key=True)
    user_id = db.Column(db.String(50), primary_key=True)
    user_name = db.Column(db.String(20))
    password = db.Column(db.String(50))
    email = db.Column(db.String(50))

    def __init__(self, employee_id=None, user_id=None, user_name=None, password=None, email=None):
        self.employee_id = employee_id
        self.user_id = user_id
        self.user_name = user_name
        self.password = password
        self.email = email

    def __repr__(self):
        return '<Entry employee_id:{} user_id:{}>'.format(self.employee_id, self.user_id)
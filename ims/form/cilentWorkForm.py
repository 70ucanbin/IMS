from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

class ClientWorkForm(FlaskForm):
    employee_id = StringField()
    orderCd = StringField('オーダー番号', validators=[DataRequired()])
    taskCd = StringField('taskCd', validators=[DataRequired()])
    subOrderCd = StringField('subOrderCd', validators=[DataRequired()])
    workHours = StringField('workHours', validators=[DataRequired()])
    workMinutes = StringField('workMinutes', validators=[DataRequired()])
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, HiddenField, FloatField, DecimalField
from wtforms.validators import DataRequired, InputRequired, Required
from wtforms.widgets import TextArea


class MonthlyReportForm(FlaskForm):
    workDetails = StringField('作業内容', validators=[Required(message='作業内容は必須です。')])
    startWorkHours = SelectField('出勤時間(時)', validators=[InputRequired(message="")], choices= [], coerce= int)
    startWorkMinutes = SelectField('出勤時間(分)', validators=[InputRequired(message="")], choices= [], coerce= int)
    endWorkHours = SelectField('退勤時間(時)', validators=[InputRequired(message="")], choices= [], coerce= int)
    endWorkMinutes = SelectField('退勤時間(分)', validators=[InputRequired(message="")], choices= [], coerce= int)
    normalWorkingHours = DecimalField('通常勤務時間', default=0)
    overtimeHours = DecimalField('残業時間数', default=0)
    holidayWork_hours = DecimalField('休日出勤時間', default=0)
    note = StringField('備考', widget=TextArea())
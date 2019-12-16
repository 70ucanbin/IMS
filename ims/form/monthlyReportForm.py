from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, DecimalField
from wtforms.validators import InputRequired, Length
from wtforms.widgets import TextArea


class MonthlyReportForm(FlaskForm):
    workDetails = StringField('作業内容', [InputRequired(message='作業内容は必須です。')])
    startWorkHours = SelectField('出勤時刻(時)', [InputRequired(message='出勤時刻(時)は必須です。')], choices= [], coerce= int)
    startWorkMinutes = SelectField('出勤時刻(分)', [InputRequired(message='出勤時刻(分)は必須です。')], choices= [], coerce= int)
    endWorkHours = SelectField('退勤時刻(時)', [InputRequired(message='退勤時刻(時)は必須です。')], choices= [], coerce= int)
    endWorkMinutes = SelectField('退勤時刻(分)', [InputRequired(message='退勤時刻(分)は必須です。')], choices= [], coerce= int)
    normalWorkingHours = DecimalField(
        '通常勤務時間',
        [InputRequired(message='通常勤務時間がない場合は0を入力してください')], 
        default=0
    )
    overtimeHours = DecimalField(
        '残業時間', 
        [InputRequired(message='残業時間がない場合は0を入力してください')], 
        default=0
    )
    holidayWorkHours = DecimalField(
        '休日出勤時間', 
        [InputRequired(message='休日出勤時間がない場合は0を入力してください')], 
        default=0
    )
    note = StringField('備考', [Length(max=200, message='備考は200文字以内で入力してください。')], widget=TextArea())
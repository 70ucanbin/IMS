from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, HiddenField
from wtforms.validators import DataRequired, InputRequired, Optional
from wtforms.widgets import TextArea


class ClientWorkForm(FlaskForm):
    clientWorkId = HiddenField()
    orderCd = SelectField('オーダー番号', validators=[InputRequired(message='オーダー番号は必須です。')], choices= [], coerce= str)
    taskCd = SelectField('タスク番号', validators=[InputRequired(message='タスク番号は必須です。')], choices= [('001', '詳細工程'),('002', 'PG工程')], coerce= str)
    subOrderCd = SelectField('サブオーダー番号', choices = [('','')], validators=[Optional()])
    workHours = SelectField('稼働時間(時)', validators=[InputRequired(message="稼働時間(時)は必須です。")], choices= [], coerce= int)
    workMinutes = SelectField('稼働時間(分)', validators=[InputRequired(message="稼働時間(分)は必須です。")], choices= [], coerce= int)
    note = StringField('備考', widget=TextArea())
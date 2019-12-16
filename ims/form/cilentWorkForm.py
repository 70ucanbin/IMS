from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, HiddenField
from wtforms.validators import DataRequired, InputRequired, Optional, Length
from wtforms.widgets import TextArea


class ClientWorkForm(FlaskForm):
    clientWorkId = HiddenField()
    orderCd = SelectField('オーダー番号', [InputRequired(message='オーダー番号は必須です。')], choices= [], coerce= str)
    taskCd = SelectField('タスク番号', [InputRequired(message='タスク番号は必須です。')], choices= [('001', '詳細工程'),('002', 'PG工程')], coerce= str)
    subOrderCd = SelectField('サブオーダー番号', [Optional()], choices = [('','')], default='')
    workHours = SelectField('稼働時間(時)', [InputRequired(message="稼働時間(時)は必須です。")], choices= [], coerce= int)
    workMinutes = SelectField('稼働時間(分)', [InputRequired(message="稼働時間(分)は必須です。")], choices= [], coerce= int)
    note = StringField('備考', [Length(max=200, message='備考は200文字以内で入力してください。')], widget=TextArea())
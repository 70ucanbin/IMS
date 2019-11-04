from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, HiddenField
from wtforms.validators import DataRequired, InputRequired
from wtforms.widgets import TextArea


class ClientWorkForm(FlaskForm):
    clientWorkId = HiddenField()
    orderCd = SelectField('オーダー番号')
    taskCd = SelectField('タスク番号')
    subOrderCd = SelectField('サブオーダー番号')
    workHours = SelectField('稼働時間(時)', validators=[InputRequired(message="")], choices= [], coerce= int)
    workMinutes = SelectField('稼働時間(分)', validators=[InputRequired(message="")], choices= [], coerce= int)
    note = StringField('備考', widget=TextArea())
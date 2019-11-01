from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, HiddenField
from wtforms.validators import DataRequired, InputRequired
from wtforms.widgets import TextArea


class ClientWorkForm(FlaskForm):
    clientWorkId = HiddenField()
    orderCd = SelectField('オーダー番号', coerce=str, validators=[InputRequired(message='オーダー番号は必須です。')])
    taskCd = SelectField('タスク番号', validators=[InputRequired(message='オーダー番号は必須です。')])
    subOrderCd = SelectField('サブオーダー番号', validators=[InputRequired(message='オーダー番号は必須です。')])
    workHours = SelectField('稼働時間(時)', validators=[InputRequired])
    workMinutes = SelectField('稼働時間(分)', validators=[InputRequired])
    note = StringField('備考', widget=TextArea())
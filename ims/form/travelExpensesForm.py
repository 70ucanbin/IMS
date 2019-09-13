from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import IntegerField, StringField, PasswordField, FileField, HiddenField
from wtforms.validators import Required
from wtforms.widgets import TextArea

class TravelExpensesForm(FlaskForm):
    travelExpensesId = HiddenField()
    expenseDate = StringField('月日', validators=[Required(message='月日は必須です。')])
    expenseItem = StringField('費目', validators=[Required(message='費目は必須です。')])
    route = StringField('ルート/詳細')
    transit = StringField('交通手段/詳細')
    payment = StringField('金額', validators=[Required(message='金額は必須です。')])
    uploadFile = FileField()
    note = StringField('備考', widget=TextArea())
from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, FileField, HiddenField
from wtforms.validators import Required, ValidationError
from wtforms.widgets import TextArea

class TravelExpensesForm(FlaskForm):
    travelExpensesId = HiddenField()
    expenseDate = StringField('月日', [Required(message='月日は必須です。')])
    expenseItem = StringField('費目', [Required(message='費目は必須です。')])
    route = StringField('ルート/詳細')
    transit = StringField('交通手段/詳細')
    payment = StringField('金額', [Required(message='金額は必須です。')])
    uploadFile = FileField()
    note = StringField('備考', widget=TextArea())

    def validate_payment(self, payment):
        if len(payment.data) > 11:
            raise ValidationError('金額は9桁以下の数字で記入してください。')
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, PasswordField, validators
from wtforms.fields.html5 import EmailField
from wtforms.validators import InputRequired, ValidationError

class UserForm(FlaskForm):
    userId = StringField('ユーザID',[validators.Length(min=4, max=25, message=u'4-25文字で入力してください。')])
    password = PasswordField('パスワード')
    confirmPassword = PasswordField('パスワードを確認する')
    groupCd = SelectField('所属部署', validators=[InputRequired(message='所属部署です。')], choices= [], coerce= str)
    role = SelectField('権限', validators=[InputRequired(message='権限は必須です。')], choices= [(1, '一般ユーザ'),(2, '部長'),(3, '管理者')], coerce= int)
    email = EmailField('メールアドレス', [validators.DataRequired(message='メールアドレスは必須です。'), validators.Email(message='メールアドレスは正しくありません。')])


    # def __init__(self, is_update=True):
    #     self.is_update = is_update


    # def validate_password(self, password):
    #     if self.is_update:
    #         pass
    #     if len(password.data) < 8 or len(password.data) > 25:
    #         raise ValidationError('パスワードは8-25文字で入力してください。')
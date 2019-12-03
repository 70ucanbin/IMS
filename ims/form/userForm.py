from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.validators import InputRequired, ValidationError, EqualTo, Email, Length

class LoginForm(FlaskForm):
    userId = StringField('ユーザID')
    password = PasswordField('パスワード')
    
class UserForm(FlaskForm):
    userId = StringField('ユーザID',[Length(min=4, max=20, message='4-20文字で入力してください。')])
    userName = StringField('ユーザ名',[Length(min=1, max=20, message='1-20文字以内で入力してください。')])
    password = PasswordField(
        'パスワード', [
        EqualTo('confirmPassword', message='パスワードは一致しません。'),
        InputRequired(message='パスワードは必須です。')
        ])
    confirmPassword = PasswordField('パスワードを確認する', [InputRequired(message='パスワードの確認は必須です。')])
    groupId = SelectField('所属部署', [InputRequired(message='所属部署は必須です。')], choices= [], coerce= str)
    role = SelectField('権限', [InputRequired(message='権限は必須です。')], choices= [(1, '一般ユーザ'),(2, '部長'),(3, '管理者')], coerce= int)
    email = EmailField('メールアドレス', [InputRequired(message='メールアドレスは必須です。'), Email(message='メールアドレスは正しくありません。')])

    def validate_password(self, password):
        if len(password.data) < 8 or len(password.data) > 20:
            raise ValidationError('パスワードは8-20文字で入力してください。')
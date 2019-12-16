from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.validators import InputRequired, EqualTo, Email, Length

class LoginForm(FlaskForm):
    userId = StringField('ユーザID')
    password = PasswordField('パスワード')
    
class MyPageForm(FlaskForm):
    userName = StringField(
        'ユーザ名',
        [InputRequired(message='ユーザ名は必須です。'), 
        Length(min=1, max=20, message='ユーザ名は1-20文字以内で入力してください。')]
        )
    password = PasswordField(
        'パスワード', [
        Length(min=8, max=20, message='パスワードは8-20文字で入力してください。'),
        EqualTo('confirmPassword', message='パスワードは一致しません。'),
        InputRequired(message='パスワードは必須です。')
        ])
    confirmPassword = PasswordField('パスワードを確認する', [InputRequired(message='パスワードの確認は必須です。')])
    email = EmailField(
        'メールアドレス', 
        [InputRequired(message='メールアドレスは必須です。'), 
        Email(message='メールアドレスは正しくありません。')]
        )

class UserForm(MyPageForm):
    userId = StringField(
        'ユーザID',
        [InputRequired(message='ユーザIDは必須です。'), 
        Length(min=4, max=20, message='ユーザIDは4-20文字で入力してください。')]
        )
    groupId = SelectField(
        '所属部署', 
        [InputRequired(message='所属部署は必須です。')], 
        choices= [], 
        coerce= str
        )
    role = SelectField(
        '権限', 
        [InputRequired(message='権限は必須です。')], 
        choices= [(1, '一般ユーザ'),(2, '部長'),(3, '管理者')], 
        coerce= int)

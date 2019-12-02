from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, PasswordField, validators
from wtforms.fields.html5 import EmailField
from wtforms.validators import InputRequired, Required, ValidationError, EqualTo

class LoginForm(FlaskForm):
    userId = StringField('ユーザID')
    password = PasswordField('パスワード')
    
class UserForm(FlaskForm):
    userId = StringField('ユーザID',[validators.Length(min=4, max=20, message=u'4-20文字で入力してください。')])
    userName = StringField('ユーザ名',[validators.Length(max=20, message=u'20文字以内で入力してください。')])
    password = PasswordField(
        'パスワード', 
        validators=[
            EqualTo('confirmPassword', message='パスワードは一致しません。'),
            Required(message='パスワードは必須です。')])
    confirmPassword = PasswordField('パスワードを確認する', validators=[Required(message='パスワードの確認は必須です。')])
    groupId = SelectField('所属部署', validators=[InputRequired(message='所属部署は必須です。')], choices= [], coerce= str)
    role = SelectField('権限', validators=[InputRequired(message='権限は必須です。')], choices= [(1, '一般ユーザ'),(2, '部長'),(3, '管理者')], coerce= int)
    email = EmailField('メールアドレス', [validators.DataRequired(message='メールアドレスは必須です。'), validators.Email(message='メールアドレスは正しくありません。')])

    def validate_password(self, password):
        if len(password.data) < 8 or len(password.data) > 20:
            raise ValidationError('パスワードは8-20文字で入力してください。')
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators

class UserForm(FlaskForm):
    userId = StringField('ユーザID',[validators.Length(min=4, max=25, message=u'4-25文字で入力してください.')])
    password = PasswordField('パスワード',[validators.Length(min=8, max=25, message=u'4-25文字で入力してください.')])
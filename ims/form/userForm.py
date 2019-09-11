from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators
from wtforms.validators import DataRequired

class UserForm(FlaskForm):
    userId = StringField('userId',[validators.Length(min=4, max=25, message=u'4-25文字で入力してください.')])
    password = PasswordField('password',[validators.Length(min=4, max=25, message=u'4-25文字で入力してください.')])
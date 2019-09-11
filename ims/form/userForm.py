from flask_wtf import FlaskForm
from wtforms import StringField, validators
from wtforms.validators import DataRequired

class UserForm(FlaskForm):
    userId = StringField('user name',  [validators.Length(min=4, max=25, message=u'4-25文字で入力してください.')])
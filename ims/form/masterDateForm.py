from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField, validators
from wtforms.validators import DataRequired, InputRequired, Required

class MasterDataForm(FlaskForm):
    itemCategory = SelectField('カテゴリー', validators=[InputRequired(message="カテゴリーは必須です。")], choices= [], coerce= str)
    itemCD = StringField('コード', [validators.Length(max=20, message=u'20文字で入力してください。')])
    itemValue = StringField('名称', [validators.Length(max=100, message=u'100文字で入力してください。')])
    displayOrder = IntegerField('表示順')
    isActive = StringField('表示/非表示')

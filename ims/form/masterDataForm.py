from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField, RadioField, HiddenField
from wtforms.validators import InputRequired, Required, Length

class MasterDataForm(FlaskForm):
    itemId = HiddenField()
    itemCategory = SelectField(
        'カテゴリー', 
        [InputRequired(message='カテゴリーは必須です。')], 
        choices= [], 
        coerce= str
        )
    itemCD = StringField(
        'コード', 
        [InputRequired(message='コードは必須です。'), 
        Length(max=20, message=u'コードは20文字以内で入力してください。')]
        )
    itemValue = StringField(
        '名称', 
        [InputRequired(message='名称は必須です。'), 
        Length(max=100, message=u'名称は100文字以内で入力してください。')]
        )
    displayOrder = IntegerField(
        '表示順', 
        [InputRequired(message='表示順は必須です。')]
        )
    isActive = RadioField(choices=[(1,'有効'), (0,'無効')], default=True, coerce= int)

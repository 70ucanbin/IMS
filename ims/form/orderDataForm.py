from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField, validators, RadioField, HiddenField
from wtforms.validators import DataRequired, InputRequired, Required

class OrderDataForm(FlaskForm):
    orderId = HiddenField()
    clientCd = SelectField('客先', validators=[InputRequired(message='客先は必須です。')], choices= [], coerce= str)
    groupCd = StringField('所属部署')
    orderCd = StringField('件名コード', [validators.Length(max=20, message=u'20文字で入力してください。')])
    orderValue = StringField('件名', [validators.Length(max=100, message=u'100文字で入力してください。')])
    displayOrder = IntegerField('表示順')
    isActive = RadioField(choices=[(1,'有効'), (0,'無効')], default=True, coerce= int)

class SubOrderDataForm(FlaskForm):
    subOrderId = HiddenField()
    clientCd = SelectField('客先', validators=[InputRequired(message='客先は必須です。')], choices= [], coerce= str)
    groupCd = StringField('所属部署')
    orderCd = SelectField('件名', validators=[InputRequired(message='件名は必須です。')], choices= [], coerce= str)
    subOrderCd = StringField(
        'サブオーダーコード', 
        [InputRequired(message='サブオーダーコードは必須です。'), 
        validators.Length(max=20, message=u'20文字で入力してください。')]
        )
    subOrderValue = StringField(
        'サブオーダー名', 
        [InputRequired(message='サブオーダー名は必須です。'), 
        validators.Length(max=100, message=u'100文字で入力してください。')]
        )
    displayOrder = IntegerField('表示順', [InputRequired(message='表示順は必須です。')])
    isActive = RadioField(choices=[(1,'有効'), (0,'無効')], default=True, coerce= int)

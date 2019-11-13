from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators

class MasterDataForm(FlaskForm):
    itemCD = StringField('コード', [validators.Length(max=20, message=u'20文字で入力してください.')])
    itemValue = StringField('名称', [validators.Length(max=100, message=u'100文字で入力してください.')])
    displayOrder = StringField('表示順')
    isActive = StringField('表示/非表示')

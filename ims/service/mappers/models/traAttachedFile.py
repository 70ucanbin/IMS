from ims import db

class TraAttachedFile(db.Model):
    __tablename__ = 'tra_attached_file'
    attached_file_id = db.Column(db.String(20), primary_key=True)
    file_name = db.Column(db.String(20))
    file_size = db.Column(db.Integer)
    file_data = db.Column(db.LargeBinary)

    def __init__(self, attached_file_id=None, file_name=None, file_size=None, file_data=None):
        self.attached_file_id = attached_file_id
        self.file_name = file_name
        self.file_size = file_size
        self.file_data = file_data

    def __repr__(self):
        return '<Entry attached_file_id:{}>'.format(self.attached_file_id)
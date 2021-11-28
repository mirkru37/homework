from init import db


class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    surname = db.Column(db.String(30))
    email = db.Column(db.String(30), unique=True, nullable=False)
    hash = db.Column(db.Text, nullable=False)
    role = db.Column(db.String(10), nullable=False)

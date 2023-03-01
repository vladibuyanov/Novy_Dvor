from flask_login import UserMixin

from flask_app import db


class AdminUser(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=True)
    password = db.Column(db.String(50), nullable=True)

    def __repr__(self):
        return self.name

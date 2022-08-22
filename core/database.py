from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from core.flask_app import app

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class AdminUser(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=True)
    password = db.Column(db.String(50), nullable=True)

    def __repr__(self):
        return self.name


class Objects(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    txt = db.Column(db.Text)
    src = db.Column(db.Text)

    def __repr__(self):
        return '<Name %r>' % self.name


class Items(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    price = db.Column(db.String(5), nullable=False)
    about = db.Column(db.Text, nullable=False)
    src = db.Column(db.Text, nullable=False)
    isActive = db.Column(db.Boolean, nullable=True)

    def __repr__(self):
        return self.title

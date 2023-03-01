from flask_app import db


class Items(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    price = db.Column(db.String(5), nullable=False)
    about = db.Column(db.Text, nullable=False)
    src = db.Column(db.Text, nullable=False)
    isActive = db.Column(db.Boolean, nullable=True)

    def __repr__(self):
        return self.title

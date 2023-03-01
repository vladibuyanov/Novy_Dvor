from flask_app import db


class Objects(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    txt = db.Column(db.Text)
    src = db.Column(db.Text)

    def __repr__(self):
        return '<Name %r>' % self.name

from flask_app import db


class Items(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    price = db.Column(db.String(5), nullable=False)
    amount = db.Column(db.Integer, nullable=True)
    isActive = db.Column(db.Boolean, nullable=True)
    about = db.Column(db.Text, nullable=False)
    src = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return self.title


class OrderItems(db.Model):
    __tablename__ = 'order_items'

    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)

    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)

    def __repr__(self):
        return f"Item {self.item_id} in order {self.order_id}"


class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    customer_email = db.Column(db.String(50), nullable=False, default='none')

    items = db.relationship(
        'Items', secondary='order_items', lazy='subquery',
        backref=db.backref('orders', lazy=True)
    )

    def __repr__(self):
        return f'Order #{self.id}'

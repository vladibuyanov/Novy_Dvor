import random
from flask import session

from flask_app.core.extensions import db
from flask_app.core.models.item import Items, Order, OrderItems

"""
    TODO:
    1. User want buy more items than we have
    2. Session id
"""


def shop_view_func(request) -> None:
    if request.method == 'GET':
        if 'card' not in session:
            session['id'] = random.randint(1, 10000)
            session['card'] = dict()
    else:
        add_in_cart_func(request.form['id'])
    session.modified = True


def add_in_cart_func(product) -> None:
    if product not in session['card']:
        session['card'][product] = 1
    else:
        session['card'][product] += 1
    session.modified = True


def cart_remove_func(request) -> None:
    delete_items = request.form['product_id']
    del session['card'][delete_items]
    session.modified = True


def cart_func() -> tuple:
    ordered_items_dict = session.get('card', [])
    try:
        ordered_items = Items.query.filter(Items.id.in_(ordered_items_dict.keys())).all()
        ordered_items_with_count = [
            [
                item,  # Model of item
                ordered_items_dict[str(item.id)],  # Amount
                int(item.price) * ordered_items_dict[str(item.id)]  # Price
            ]
            for item in ordered_items
        ]
        total_price = sum(pair[2] for pair in ordered_items_with_count)
        return ordered_items_with_count, total_price
    except AttributeError:
        return None, None


def cart_new_order_func(ordered_items_with_count):
    order = Order()
    db.session.add(order)
    db.session.commit()
    session['order'] = order.id
    for ordered_item_with_count in ordered_items_with_count:
        item_id = ordered_item_with_count[0].id
        count = ordered_item_with_count[1]
        added_item = OrderItems(item_id=item_id, quantity=count, order_id=order.id)
        db.session.add(added_item)
        db.session.commit()
    return order.id


def finish_order_func(order_id, request):
    # Add email to Order model
    order = Order.query.get(order_id)
    order.customer_email = request.form['email']
    db.session.commit()

    # Preparing data for transfer to the payment service
    cart = cart_func()
    order_dict = {
        'email': order.customer_email,
        'total price': cart[1],
    }
    for order_items in cart[0]:
        order_dict[order_items[0].title] = [order_items[1], order_items[2]]
        order_items[0].amount = order_items[0].amount - order_items[1]
        db.session.commit()

    session.clear()
    session.new = True

    return order_dict

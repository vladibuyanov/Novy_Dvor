import random

from flask import Blueprint, render_template, session, request, redirect, url_for
from flask_app.core.extensions import db
from flask_app.core.models.item import Items

from flask_app.core.func import add_in_cart_func, cart_func


shop = Blueprint('shop', __name__)
template_path = 'shop'
redirect_template = 'shop.shop_view'


@shop.route('/shop', methods=['GET', 'POST'])
def shop_view():
    template = f'{template_path}/shop.html'
    res = db.session.query(Items).all()

    if request.method == 'GET':
        if 'card' not in session:
            session['id'] = random.randint(1, 10000)
            session['card'] = dict()
    else:
        add_in_cart_func(request.form['id'])
    session.modified = True
    return render_template(template, res=res)


@shop.route('/shop/item/<int:item_id>', methods=['GET', 'POST'])
def item_view(item_id):
    template = f'{template_path}/shop_item.html'
    res = Items.query.get(item_id)

    if request.method == 'GET':
        return render_template(template, res=res)
    else:
        add_in_cart_func(request.form['id'])
        session.modified = True
        return redirect(url_for(redirect_template))


@shop.route('/cart/', defaults={'user_cart_id': None})
@shop.route('/cart/<user_cart_id>')
def cart_view(user_cart_id):
    template = f'{template_path}/shop_cart.html'

    if user_cart_id is None:
        return render_template(template)
    else:
        ordered_items_with_count, total_price = cart_func()
        return render_template(template, cart=ordered_items_with_count, total=total_price)


@shop.route('/cart/send', methods=['POST'])
def send():
    session.clear()
    session.new = True
    return redirect(url_for(redirect_template))

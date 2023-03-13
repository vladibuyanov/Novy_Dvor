from flask import Blueprint, render_template, session, request, redirect, url_for, Response, jsonify
from flask_app.core.extensions import db
from flask_app.core.models.item import Items

from flask_app.core.func import *

shop = Blueprint('shop', __name__)
template_path = 'shop'
redirect_template = 'shop.shop_view'


@shop.route('/shop', methods=['GET', 'POST'])
def shop_view():
    template = f'{template_path}/shop.html'
    res = db.session.query(Items).all()
    shop_view_func(request)
    return render_template(template, res=res)


@shop.route('/shop/item/<int:item_id>', methods=['GET', 'POST'])
def item_view(item_id):
    template = f'{template_path}/shop_item.html'
    if request.method == 'GET':
        return render_template(template, res=Items.query.get(item_id))
    else:
        add_in_cart_func(request.form['id'])
        return redirect(url_for(redirect_template))


@shop.route('/cart/', defaults={'user_cart_id': None})
@shop.route('/cart/<user_cart_id>', methods=['GET', 'POST'])
def cart_view(user_cart_id):
    template = f'{template_path}/shop_cart.html'
    ordered_items_with_count, total_price = cart_func()

    if request.method == 'GET':
        cart = ordered_items_with_count if user_cart_id else None
        total = total_price if user_cart_id else None
        return render_template(template, cart=cart, total=total)

    else:
        # Remove from cart
        if request.path == '/cart/remove':
            cart_remove_func(request)
            return redirect(url_for(redirect_template))
        # Finish order
        elif request.path == '/cart/finish_order':
            if 'order' in session:
                return redirect(url_for('shop.finish_order_view', order_id=session['order']))
            else:
                # Make new order
                order_id = cart_new_order_func(ordered_items_with_count)
                return redirect(url_for('shop.finish_order_view', order_id=order_id))


@shop.route('/cart/finish_order/<int:order_id>', methods=['GET', 'POST'])
def finish_order_view(order_id):
    template = f'{template_path}/shop_finish_order.html'
    if request.method == 'GET':
        return render_template(template)
    else:
        finish_order = finish_order_func(order_id, request)
        return render_template(template, finish_order=finish_order)

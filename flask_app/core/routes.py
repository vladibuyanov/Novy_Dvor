import random

from flask import Blueprint, render_template, session, request, redirect, url_for
from flask_login import login_user, logout_user, login_required

from flask_app.core.extensions import db
from flask_app.core.models.admin import AdminUser
from flask_app.core.models.item import Items
from flask_app.core.models.objects import Objects


main = Blueprint('main', __name__)


@main.route('/', methods=['GET'])
@main.route('/main')
def index():
    template = 'index.html'
    return render_template(template)


@main.route('/shop', methods=['GET', 'POST'])
def shop():
    template = 'shop/shop.html'
    res = db.session.query(Items).all()

    if 'cart' not in session:
        session['id'] = random.randint(1, 10000)
        session['cart'] = []
    if request.method == 'POST':
        session['cart'].append(request.form['id'])
        session.modified = True
    return render_template(template, res=res)


@main.route('/shop/<int:item_id>', methods=['GET', 'POST'])
def item_page(item_id):
    template = 'shop/shop_item.html'
    redirect_template = 'shop'
    res = Items.query.filter_by(id=item_id).first()

    if request.method == 'POST':
        session['cart'].append(request.form['id'])
        session.modified = True
        return redirect(url_for(redirect_template))
    return render_template(template, res=res)


@main.route('/cart/<int:user_cart_id>')
def cart(user_cart_id):
    template = 'shop/shop_cart.html'
    user_cart = list()
    total = 0

    if session['id'] == user_cart_id:
        if 'cart' in session:
            for item in session['cart']:
                user_cart.append(Items.query.filter_by(id=item).first())
                total += int(Items.query.filter_by(id=item).first().price)
            return render_template(template, cart=user_cart, items_number=len(user_cart))
        else:
            return render_template(template, items_number=len(user_cart))
    else:
        return render_template(template, items_number=len(user_cart))


@main.route('/cart/send')
def send():
    redirect_template = 'shop'
    session.clear()
    session.new = True

    return redirect(url_for(redirect_template))


@main.route('/objects')
def objects():
    template = 'objects.html'
    res = db.session.query(Objects).all()

    return render_template(template, res=res)


@main.route('/objects/<int:object_id>')
def object_page(object_id):
    template = 'object.html'
    if object_id:
        res = Objects.query.filter_by(id=object_id).first()

        return render_template(template, res=res)


@main.route('/login', methods=['GET', 'POST'])
def admin_login():
    template = 'admin/login_admin.html'
    redirect_template = 'admin.index'

    if request.method != 'POST':
        return render_template(template)
    else:
        name = request.form['name']
        password = request.form['password']
        login_admin = AdminUser.query.filter_by(name=name).first()
        if login_admin:
            if password == login_admin.password:
                login_user(login_admin)
                return redirect(url_for(redirect_template))
            else:
                return render_template(template)
        else:
            return render_template(template)


@main.route('/logout', methods=['GET'])
@login_required
def logo():
    redirect_template = 'index'
    logout_user()
    return redirect(url_for(redirect_template))

import random

from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user, current_user
from flask_migrate import Migrate
from flask_admin import Admin, expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView


app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(user_id):
    return AdminUser.query.get(user_id)


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
        return f'{self.title}'


class DashBoardView(AdminIndexView):

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('index'))

    @expose('/')
    def admin_panel(self):
        return self.render('admin/dashboard_index.html')


class MyModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('index'))


admin = Admin(app, name="Novy Dvor", template_mode='bootstrap4', index_view=DashBoardView(), endpoint='admin')
admin.add_view(MyModelView(AdminUser, db.session))
admin.add_view(MyModelView(Objects, db.session))
admin.add_view(MyModelView(Items, db.session))


@app.route('/', methods=['GET'])
@app.route('/main')
def index():
    return render_template('index.html')


@app.route('/shop', methods=['GET', 'POST'])
def shop():
    res = db.session.query(Items).all()
    if 'cart' not in session:
        session['id'] = random.randint(1, 10000)
        session['cart'] = []
    if request.method == 'POST':
        session['cart'].append(request.form['id'])
        session.modified = True
    return render_template('shop/shop.html', res=res)


@app.route('/shop/<int:item_id>', methods=['GET', 'POST'])
def item_page(item_id):
    res = Items.query.filter_by(id=item_id).first()
    if request.method == 'POST':
        session['cart'].append(request.form['id'])
        session.modified = True
        return redirect(url_for('shop'))
    return render_template('shop/shop_item.html', res=res)


@app.route('/cart/<int:user_cart_id>')
def cart(user_cart_id):
    user_cart = list()
    total = 0
    if session['id'] == user_cart_id: 
        if 'cart' in session:
            for item in session['cart']:
                user_cart.append(Items.query.filter_by(id=item).first())
                total += int(Items.query.filter_by(id=item).first().price)
            return render_template('shop/shop_cart.html', cart=user_cart, items_number=len(user_cart))
        else:
            return render_template('shop/shop_cart.html', items_number=len(user_cart))
    else:
        return render_template('shop/shop_cart.html', items_number=len(user_cart))


@app.route('/cart/send')
def send():
    session.clear()
    session.new = True
    return redirect(url_for('shop'))


@app.route('/objects')
def objects():
    res = db.session.query(Objects).all()
    return render_template('objects.html', res=res)


@app.route('/objects/<int:object_id>')
def object_page(object_id):
    if object_id:
        res = Objects.query.filter_by(id=object_id).first()
        return render_template('object.html', res=res)


@app.route('/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        login_admin = AdminUser.query.filter_by(name=name).first()
        if login_admin:
            if password == login_admin.password:
                login_user(login_admin)
                return redirect(url_for('admin.index'))
            else:
                return render_template('admin/login_admin.html')
        else:
            return render_template('admin/login_admin.html')
    return render_template('admin/login_admin.html')


@app.route('/logout', methods=['GET'])
@login_required
def logo():
    logout_user()
    return redirect(url_for('index'))

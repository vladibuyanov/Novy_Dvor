from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, logout_user, login_required
from flask_app.core.models.admin import AdminUser


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def admin_login():
    template = 'admin/login_admin.html'
    redirect_template = 'admin.index'

    if request.method != 'POST':
        return render_template(template)
    else:
        name = request.form['name']
        password = request.form['password']
        login_admin = AdminUser.query.filter_by(name=name).first()

        if not login_admin or password != login_admin.password:
            return render_template(template)
        else:
            if password == login_admin.password:
                login_user(login_admin)
                return redirect(url_for(redirect_template))


@auth.route('/logout', methods=['GET'])
@login_required
def logo():
    redirect_template = 'index'
    logout_user()
    return redirect(url_for(redirect_template))

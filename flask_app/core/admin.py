from flask_admin import expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask import redirect, url_for



class DashBoardView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('main.index'))

    @expose('/')
    def admin_panel(self):
        return self.render('admin/dashboard_index.html')


class MyModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('main.index'))


class OrderItemsAdmin(MyModelView):
    column_list = ['id', 'quantity', 'item_id', 'order_id']


class OrderAdmin(MyModelView):
    column_list = ['id', 'customer_email']

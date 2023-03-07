from flask import Flask
from flask_login import LoginManager
from flask_admin import Admin

from flask_app.core.admin import DashBoardView, MyModelView
from flask_app.core.extensions import db, migrate
from flask_app.core.models.admin import AdminUser
from flask_app.core.models.item import Items
from flask_app.core.models.objects import Objects

from flask_app.core.routes.main import main
from flask_app.core.routes.auth import auth
from flask_app.core.routes.area_objects import area_objects
from flask_app.core.routes.shop import shop


def create_app(config_file_path):
    app = Flask(__name__)
    app.config.from_pyfile(config_file_path)
    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)
    login_manager = LoginManager(app, db)

    @login_manager.user_loader
    def load_user(user_id):
        return AdminUser.query.get(user_id)

    """ Admin panel"""
    admin = Admin(
        app, name="Novy Dvor", template_mode='bootstrap4',
        index_view=DashBoardView(), endpoint='admin'
    )
    admin.add_view(MyModelView(AdminUser, db.session))
    admin.add_view(MyModelView(Objects, db.session))
    admin.add_view(MyModelView(Items, db.session))

    # Routes
    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(area_objects)
    app.register_blueprint(shop)

    return app


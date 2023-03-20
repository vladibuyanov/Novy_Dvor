from flask import render_template, Blueprint

extensions = Blueprint('extensions', __name__)


@extensions.app_errorhandler(404)
def page_not_found(e):
    return render_template('extensions/404.html'), 404

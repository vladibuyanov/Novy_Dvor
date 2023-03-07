from flask import Blueprint, render_template


main = Blueprint('main', __name__)


@main.route('/', methods=['GET'])
@main.route('/main')
def index():
    template = 'index.html'
    return render_template(template)

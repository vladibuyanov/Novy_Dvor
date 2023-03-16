from flask import Blueprint, render_template

from flask_app.forms.ContactForm import ContactForm

main = Blueprint('main', __name__)


@main.route('/', methods=['GET'])
@main.route('/main')
def index():
    template = 'index.html'
    contact_form = ContactForm()
    return render_template(template, form=contact_form)

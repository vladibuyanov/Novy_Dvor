from flask import Blueprint, render_template, request, redirect

from flask_app.core.forms.ContactForm import ContactForm

main = Blueprint('main', __name__)


@main.route('/', methods=['GET', 'POST'])
@main.route('/main')
def index():
    template = 'index.html'
    contact_form = ContactForm()

    if request.method == 'GET':
        return render_template(template, form=contact_form)
    else:
        email = contact_form.data['email']
        message = contact_form.data['message']
        print(email, message)
        return redirect('main')

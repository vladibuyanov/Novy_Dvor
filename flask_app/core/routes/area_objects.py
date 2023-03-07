from flask import Blueprint, render_template
from flask_app.core.extensions import db
from flask_app.core.models.objects import Objects


area_objects = Blueprint('area_objects', __name__)


@area_objects.route('/objects')
def objects_view():
    template = 'objects.html'
    res = db.session.query(Objects).all()

    return render_template(template, res=res)


@area_objects.route('/objects/<int:object_id>')
def object_page(object_id):
    template = 'object.html'
    res = Objects.query.get(object_id)

    return render_template(template, res=res)

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email


class ContactForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"class": "form-control"})
    message = TextAreaField('Message', validators=[DataRequired()], render_kw={"class": "form-control"})
    submit = SubmitField("Poslat'", render_kw={"class": "main-button"})

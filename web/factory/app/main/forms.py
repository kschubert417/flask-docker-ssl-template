from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField, TextAreaField
from wtforms.validators import DataRequired, Email

class ContactUsForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name')
    email = EmailField('Email Address', validators=[DataRequired(), Email('Please enter a valid email address.')])
    company = StringField('Company')
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Send message')

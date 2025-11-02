from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, SelectField
from wtforms.validators import DataRequired, Email, Optional, Length

class ManageUserForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name')
    email = EmailField('Email Address', validators=[DataRequired(), Email('Please enter a valid email address.')])
    role = SelectField('Role', choices=[('user', 'user'), ('admin', 'admin')], validators=[DataRequired()])
    password = PasswordField('Password', validators=[Optional(), Length(min=8)])
    submit = SubmitField('Save Changes')

    def __init__(self, is_create=True, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if is_create:
            self.password.validators = [DataRequired()]
        else:
            self.password.validators = []  # allow blank passwords during update
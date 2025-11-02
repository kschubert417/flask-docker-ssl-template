from datetime import date
# from functools import wraps
from app import db
from app.main.forms import ContactUsForm
from flask import render_template, flash, redirect, url_for
from app.main import bp
from app.models import Messages

# def login_required(f):
#  @wraps(f)
#  def decorated_function(*args, **kwargs):
#      if 'user' not in session:
#          return redirect(url_for('auth.login'))
#      return f(*args, **kwargs)
#  return decorated_function

@bp.route('/', methods=['GET', 'POST'])
def index():
    form = ContactUsForm()
    alert = None
    form_submitted = False
    return render_template('index.html', alert=alert, form=form, form_submitted=form_submitted)

@bp.route('/about', methods=['GET'])
def about():
    return render_template('about.html')

@bp.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactUsForm()

    if form.validate_on_submit():
        # Create and save message
        message = Messages(
            first_name=form.firstname.data,
            last_name=form.lastname.data,
            company=form.company.data,
            email=form.email.data,
            message=form.message.data,
            date=date.today()
        )
        db.session.add(message)
        db.session.commit()
        
        flash(f"Thank you for your message, {form.firstname.data}! We will be in touch with you shortly.", "success")
        return redirect(url_for('main.contact'))  # PRG pattern

    # Form validation errors are automatically handled by WTForms
    return render_template('contact.html', form=form)
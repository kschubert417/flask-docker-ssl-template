from flask import render_template, flash, redirect, url_for
from flask_login import login_user, logout_user, current_user
from sqlalchemy import select
from datetime import datetime, timezone
from app import db
from app.models import User
from app.auth.forms import LoginForm
from app.auth import bp
# from functools import wraps
# import sqlalchemy

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        
        user = db.session.scalar(
            select(User).where(User.email == email)
        )
        
        if user is None or not user.check_password(password):
            flash("Invalid email or password. Please try again.", "danger")
            return render_template('login.html', form=form)

        # Login succesful
        user.lastlogindate = datetime.now()
        db.session.commit()

        login_user(user, remember=form.remember_me.data)
        flash("You have successfully logged in!", "success")
        return redirect(url_for('main.index'))

    return render_template('login.html', form=form)

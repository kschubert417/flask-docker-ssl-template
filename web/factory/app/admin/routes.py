from functools import wraps
from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user
from sqlalchemy import select
from app import db
from app.admin import bp
from app.admin.forms import ManageUserForm
from app.models import Messages, User

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('auth.login'))
        if current_user.role != 'admin':
            flash('Admin access required', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

@bp.route('/admin_dashboard')
@admin_required
def admin_dashboard():
    return render_template('admin_dashboard.html')


@bp.route('/message/list', methods=['GET'])
@admin_required
def message_list():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 40, type=int), 100)

    stmt = db.select(Messages)

    paginated = Messages.paginate_query(
        query=stmt,
        page=page,
        per_page=per_page,
        endpoint='admin.message_list' # needs to match blueprint endpoint
    )

    # return render_template('message_list.html', messages=obj)
    return render_template('message_list.html', messages=paginated['items'], pagination=paginated['_meta'], links=paginated['_links'])

@bp.route('/message/delete/<string:id>', methods=['DELETE'])
@admin_required
def message_delete(id):
    stmt = select(Messages).where(Messages.id == id)
    obj = db.session.scalar(stmt)
    if obj:
        db.session.delete(obj)
        db.session.commit()
        return '', 200
    else:
        print(f"Error deleting message {id}: {e}")
        return redirect(url_for('admin.message_list'))

@bp.route('/user/list', methods=['GET'])
@admin_required
def list_users():
    stmt = select(User).order_by(User.id)
    obj = db.session.scalars(stmt).all()
    return render_template('user_list.html', users=obj)

@bp.route('/user/create', methods=['GET', 'POST'])
@admin_required
def user_create():
    form = ManageUserForm(is_create=True)
    
    if form.validate_on_submit():
        user = User()
        form.populate_obj(user) # Populate user object from form data
        user.set_password(form.password.data)  # Hash the password
        db.session.add(user)
        db.session.commit()
        flash('User created successfully', 'success')
        return redirect(url_for('admin.list_users'))

    return render_template('user_add_edit.html', form=form, action='create')

@bp.route('/user/update/<string:id>', methods=['GET', 'POST'])
@admin_required
def user_update(id):
    user = db.session.get(User, id)
    if not user:
        flash("User not found", "danger")
        return redirect(url_for("admin.list_users"))

    form = ManageUserForm(obj=user, is_create=False)

    if form.validate_on_submit():
        print("FORM VALIDATED ==========================")
        form.populate_obj(user)
        if form.password.data.strip():
            user.set_password(form.password.data)
        db.session.commit()
        flash("User updated successfully", "success")
        return redirect(url_for("admin.list_users"))

    return render_template('user_add_edit.html', form=form, action='update', user=user)

@bp.route('/user/delete/<string:id>', methods=['POST', 'DELETE'])
@admin_required
def user_delete(id):
    stmt = select(User).where(User.id == id)
    user = db.session.scalar(stmt)
    if user:
        user = db.session.delete(user)
        db.session.commit()
        return '', 200
    else:
        # flash(f"Error deleting user ID {id}", 'success')
        print(f"Error deleting user ID {id}: {e}")
        return redirect(url_for('admin.list_users'))

from flask import Blueprint, render_template, url_for, redirect, flash, request, session, abort
from flask_login import login_user, logout_user, login_required

from .. import db
from .models import User
from .forms import LoginForm, RegistrationForm, EditUserForm

auth_blueprint = Blueprint('auth', __name__)
## XXX contains dirty hack for session check `is_superadmin` ##

@auth_blueprint.route('/users/add', methods=['GET', 'POST'])
@login_required
def register():
    if (session['is_superadmin'] != True):
        abort(403)
    form = RegistrationForm(request.form)
    if form.validate_on_submit():
        user = User(username=form.username.data, is_superadmin=form.is_superadmin.data, password=form.password.data)
        user.save()
        return redirect(url_for("auth.list_users"))
    elif form.is_submitted():
        flash('The given data was invalid.', 'danger')
    return render_template('auth/register.html', form=form)


@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.authenticate(form.user_id.data, form.password.data)
        if user is not None:
            login_user(user)
            session['is_superadmin'] = user.is_superadmin
            #session['login_uid'] = user.id ### can use flask-Login's current_user.get_id()
            flash('Login successful.', 'success')
            return redirect(url_for('main.index'))
        flash('Wrong user ID or password, or your login is deactivated', 'danger')
    return render_template('auth/login.html', form=form)


@auth_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You were logged out.', 'info')
    return redirect(url_for('main.index'))

@auth_blueprint.route('/users')
@login_required
def list_users():
    if (session['is_superadmin'] != True):
        abort(403)
    l_user = User.query.order_by(db.asc(User.id)).all()
    return render_template('auth/manage.html', users=l_user)

@auth_blueprint.route('/users/edit/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    if (session['is_superadmin'] != True):
        abort(403)
    uobj = User.query.filter_by(id=user_id).first()
    form = EditUserForm(obj=uobj)
    if form.validate_on_submit():
        uobj.is_superadmin = form.is_superadmin.data
        if form.password.data != "":
            uobj.password = form.password.data
        uobj.save()
        return redirect(url_for("auth.list_users"))
    elif form.is_submitted():
        flash('The given data was invalid.', 'danger')
    return render_template('auth/edit.html', form=form, uid=user_id)

@auth_blueprint.route('/users/toggle/<int:user_id>', methods=['GET', 'POST'])
@login_required
def toggle_user(user_id):
    if (session['is_superadmin'] != True):
        abort(403)
    uobj = User.query.filter_by(id=user_id).first()
    uobj.is_active = not uobj.is_active
    uobj.save()
    return redirect(url_for('auth.list_users'))


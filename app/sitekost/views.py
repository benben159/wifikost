from flask import Blueprint, render_template, url_for, redirect, flash, request, abort, session
from flask_login import login_user, logout_user, login_required

from .. import db
from .models import SiteKost, PaketInternet
from ..auth.models import User
from .forms import SiteKostForm, PaketInternetForm, SiteKostEditForm, PaketInternetEditForm

sitekost_blueprint = Blueprint('sitekost', __name__)

@sitekost_blueprint.route('/sites')
@login_required
def list_sites():
    if (session['is_superadmin'] != True):
        abort(403)
    sit = SiteKost.query.join(User, SiteKost.user_id == User.id).add_columns(SiteKost.id, SiteKost.location_id, User.username, SiteKost.nas_ipaddress, SiteKost.nas_secret, SiteKost.is_active).all()
    return render_template('sitekost/manage.html', sites=sit)

@sitekost_blueprint.route('/sites/add', methods=['GET', 'POST'])
@login_required
def add_site():
    if (session['is_superadmin'] != True):
        abort(403)
    form = SiteKostForm(request.form)
    actusr = User.query.filter_by(is_active=True).all()
    form.user_id.choices=[(u.id, u.username) for u in actusr]
    if form.validate_on_submit():
        site = SiteKost(location_id=form.location_id.data, user_id = form.user_id.data, nas_ipaddress = form.nas_ipaddress.data, nas_secret = form.nas_secret.data)
        site.save()
        return redirect(url_for('sitekost.list_sites'))
    elif form.is_submitted():
        flash('The given data was invalid.', 'danger')
    return render_template('sitekost/create.html', form=form)

@sitekost_blueprint.route('/sites/edit/<int:site_id>', methods=['GET', 'POST'])
@login_required
def edit_site(site_id):
    if (session['is_superadmin'] != True):
        abort(403)
    sit = SiteKost.query.filter_by(id=site_id).first()
    form = SiteKostEditForm(obj=sit)
    actusr = User.query.filter_by(is_active=True).all()
    form.user_id.choices=[(u.id, u.username) for u in actusr]
    if form.validate_on_submit():
        sit.location_id = form.location_id.data
        sit.nas_ipaddress = form.nas_ipaddress.data
        sit.nas_secret = form.nas_secret.data
        sit.user_id = form.user_id.data
        sit.save()
        return redirect(url_for('sitekost.list_sites'))
    elif form.is_submitted():
        flash('The given data was invalid.', 'danger')
    return render_template('sitekost/edit.html', form=form, site_id=sit.id)

@sitekost_blueprint.route('/sites/toggle/<int:site_id>', methods=['GET', 'POST'])
@login_required
def toggle_site(site_id):
    if (session['is_superadmin'] != True):
        abort(403)
    sit = SiteKost.query.filter_by(id=site_id).first()
    sit.is_active = not sit.is_active
    sit.save()
    return redirect(url_for('sitekost.list_sites'))

### PAKET INET ###

@sitekost_blueprint.route('/pakets')
@login_required
def list_pakets():
    if (session['is_superadmin'] != True):
        abort(403)
    pak = PaketInternet.query.all()
    return render_template('paketinet/manage.html', pakets=pak)


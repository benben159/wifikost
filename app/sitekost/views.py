from flask import Blueprint, render_template, url_for, redirect, flash, request, abort, session
from flask_login import login_user, logout_user, login_required, current_user

from .. import db
from .models import SiteKost, PaketInternet, WifiUser
from ..auth.models import User
from .forms import SiteKostForm, PaketInternetForm, SiteKostEditForm, PaketInternetEditForm, WifiUserForm, WifiUserEditForm

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

@sitekost_blueprint.route('/pakets/add', methods=['GET', 'POST'])
@login_required
def add_paketinet():
    if (session['is_superadmin'] != True):
        abort(403)
    form = PaketInternetForm(request.form)
    if form.validate_on_submit():
        pak = PaketInternet(name=form.name.data, bw_mbps=form.bw_mbps.data, num_devices = form.num_devices.data, renewal_days=form.renewal_days.data)
        pak.save()
        return redirect(url_for('sitekost.list_pakets'))
    elif form.is_submitted():
        flash('The given data was invalid.', 'danger')
    return render_template('paketinet/create.html', form=form)

@sitekost_blueprint.route('/pakets/edit/<int:pak_id>', methods=['GET', 'POST'])
@login_required
def edit_paketinet(pak_id):
    if (session['is_superadmin'] != True):
        abort(403)
    pak = PaketInternet.query.filter_by(id=pak_id).first()
    form = PaketInternetEditForm(obj=pak)
    if form.validate_on_submit():
        pak.bw_mbps = form.bw_mbps.data
        pak.num_devices = form.num_devices.data
        pak.renewal_days = form.renewal_days.data
        pak.save()
        return redirect(url_for('sitekost.list_pakets'))
    elif form.is_submitted():
        flash('The given data was invalid.', 'danger')
    return render_template('paketinet/edit.html', form=form, pak_id=pak.id)

@sitekost_blueprint.route('/pakets/toggle/<int:pak_id>', methods=['GET', 'POST'])
@login_required
def toggle_paketinet(pak_id):
    if (session['is_superadmin'] != True):
        abort(403)
    pak = PaketInternet.query.filter_by(id=pak_id).first()
    pak.is_active = not pak.is_active
    pak.save()
    return redirect(url_for('sitekost.list_pakets'))

### WIFI USER ###

@sitekost_blueprint.route('/hslogins')
@login_required
def list_hslogins():
    wus = WifiUser.query.join(SiteKost, WifiUser.site_id == SiteKost.id).join(PaketInternet, WifiUser.group_id == PaketInternet.id).add_columns(WifiUser.id, WifiUser.username, WifiUser.created_date, WifiUser.is_autorenew, SiteKost.location_id, PaketInternet.name).all()
    return render_template('wifiuser/manage.html', users=wus)

@sitekost_blueprint.route('/hslogins/add', methods=['GET', 'POST'])
@login_required
def add_hslogin():
    form = WifiUserForm(request.form)
    pak = PaketInternet.query.all()
    form.group_id.choices = [(p.id, p.name) for p in pak]
    sit = SiteKost.query.filter_by(is_active=True, user_id=int(current_user.get_id())).all()
    form.site_id.choices = [(s.id, s.location_id) for s in sit]
    if form.validate_on_submit():
        wus = WifiUser(username=form.username.data, plain_password=form.plain_password.data, is_autorenew=form.is_autorenew.data, group_id=form.group_id.data, site_id=form.site_id.data)
        wus.save()
        return redirect(url_for('sitekost.list_hslogins'))
    elif form.is_submitted():
        flash('The given data was invalid.', 'danger')
    return render_template('wifiuser/create.html', form=form)

@sitekost_blueprint.route('/hslogins/edit/<int:wus_id>', methods=['GET', 'POST'])
@login_required
def edit_hslogin(wus_id):
    wus = WifiUser.query.filter_by(id=wus_id).first()
    form = WifiUserEditForm(obj=wus)
    if form.validate_on_submit():
        wus.plain_password = form.plain_password.data
        wus.site_id = form.site_id.data
        wus.group_id = form.group_id.data
        wus.is_autorenew = form.is_autorenew.data
        wus.save()
        return redirect(url_for('sitekost.list_hslogins'))
    elif form.is_submitted():
        flash('The given data was invalid.', 'danger')
    return render_template('wifiuser/edit.html', form=form, wus_id=wus.id)

@sitekost_blueprint.route('/hslogins/toggle/<int:wus_id>', methods=['GET', 'POST'])
@login_required
def toggle_hslogin(wus_id):
    return render_template('wifiuser/manage.html')

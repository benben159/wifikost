from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, ValidationError, SelectField, IntegerField, BooleanField
from wtforms.validators import DataRequired, IPAddress, Optional, Length

from .models import SiteKost, PaketInternet, WifiUser

class SiteKostForm(FlaskForm):
    location_id = StringField('RADIUS Location ID', [DataRequired()])
    user_id = SelectField('Admin User', [DataRequired()], coerce=int)
    nas_ipaddress = StringField('NAS IP Address', [Optional(), IPAddress()])
    nas_secret = StringField('NAS Secret', [Optional(), Length(min=5,max=31)])
    submit = SubmitField('Add Site')

    def validate_location_id(form, field):
        if SiteKost.query.filter_by(location_id=field.data).first() is not None:
            raise ValidationError('This location ID is already exists')

    def validate_nas_ipaddress(form, field):
        if SiteKost.query.filter_by(nas_ipaddress=field.data).first() is not None:
            raise ValidationError('This IP Address is already registered to a location')

class SiteKostEditForm(FlaskForm):
    location_id = StringField('RADIUS Location ID', render_kw={'readonly':True})
    user_id = SelectField('Admin User', [DataRequired()], coerce=int)
    nas_ipaddress = StringField('NAS IP Address', [Optional(), IPAddress()])
    nas_secret = StringField('NAS Secret', [Optional(), Length(min=5,max=31)])
    submit = SubmitField('Save Site')


class PaketInternetForm(FlaskForm):
    name = StringField('Nama Paket', [DataRequired()])
    user_id = SelectField('Admin User', [DataRequired()], coerce=int)
    bw_mbps = IntegerField('Bandwidth (Mbps)', [DataRequired()])
    num_devices = IntegerField('Simultaneous Devices', [DataRequired()])
    renewal_days = IntegerField('Autorenew (days)', [DataRequired()])
    submit = SubmitField('Simpan Paket inet')

    def validate_name(form, field):
        if PaketInternet.query.filter_by(name=field.data).first() is not None:
            raise ValidationError('This paket name is already exists')

class PaketInternetEditForm(FlaskForm):
    name = StringField('Nama Paket',  render_kw={'readonly':True})
    user_id = SelectField('Admin User', [DataRequired()], coerce=int)
    bw_mbps = IntegerField('Bandwidth (Mbps)', [DataRequired()])
    num_devices = IntegerField('Simultaneous Devices', [DataRequired()])
    renewal_days = IntegerField('Autorenew (days)', [DataRequired()])
    submit = SubmitField('Simpan Paket inet')

class WifiUserForm(FlaskForm):
    username = StringField('Username', [DataRequired()])
    plain_password = StringField('Password', [DataRequired(), Length(min=6,max=16)])
    group_id = SelectField('Paket Internet', [DataRequired()], coerce=int)
    site_id = SelectField('Site', [DataRequired()], coerce=int)
    is_autorenew = BooleanField('Autorenew this username')
    submit = SubmitField('Simpan User hotspot')

    def validate_username(form, field):
        if WifiUser.query.filter_by(username=field.data).first() is not None:
            raise ValidationError('This username is already exists')

class WifiUserEditForm(FlaskForm):
    username = StringField('Username', render_kw={'readonly':True})
    plain_password = StringField('Password', [DataRequired(), Length(min=6,max=16)])
    group_id = SelectField('Paket Internet', [DataRequired()], coerce=int)
    site_id = SelectField('Site', [DataRequired()], coerce=int)
    is_autorenew = BooleanField('Autorenew this username')
    submit = SubmitField('Simpan User hotspot')

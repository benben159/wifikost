from .auth.models import User, AnonymousUser
from . import db

# Define your models here.
# You can also define them inside a package and import them here.
# This is only a convenience so that all your models are available from a single module.

class SiteKost(db.Model):

    __tablename__ = 'sites'

    id = db.Column(db.Integer, primary_key=True)
    location_id = db.Column(db.String(64), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

class PaketInternet(db.Model):

    __tablename__ = 'wifiusergroup'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    bw_mbytes = db.Column(db.Integer, nullable=False)
    num_devices = db.Column(db.Integer, nullable=False)

class WifiUser(db.Model):

    __tablename__ = 'wifiuser'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), nullable=False)
    plain_password = db.Column(db.String(16), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('wifiusergroup.id'), nullable=False)
    site_id = db.Column(db.Integer, db.ForeignKey('sites.id'), nullable=False)


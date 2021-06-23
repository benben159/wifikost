from .. import db
from ..utils import ModelMixin
from sqlalchemy.sql import func, expression

class SiteKost(db.Model, ModelMixin):

    __tablename__ = 'sites'

    id = db.Column(db.Integer, primary_key=True)
    location_id = db.Column(db.String(64), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    nas_ipaddress = db.Column(db.String(32), nullable=True)
    nas_secret = db.Column(db.String(16), nullable=True)
    is_active = db.Column(db.Boolean, server_default=expression.true())

class PaketInternet(db.Model, ModelMixin):

    __tablename__ = 'wifiusergroup'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    bw_mbps = db.Column(db.Integer, nullable=False)
    num_devices = db.Column(db.Integer, nullable=False)
    renewal_days = db.Column(db.Integer, nullable=False)

class WifiUser(db.Model, ModelMixin):

    __tablename__ = 'wifiuser'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), nullable=False)
    plain_password = db.Column(db.String(16), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('wifiusergroup.id'), nullable=False)
    site_id = db.Column(db.Integer, db.ForeignKey('sites.id'), nullable=False)
    is_active = db.Column(db.Boolean, server_default=expression.true())
    is_autorenew = db.Column(db.Boolean, server_default=expression.true())
    created_date = db.Column(db.Date, server_default=func.now())


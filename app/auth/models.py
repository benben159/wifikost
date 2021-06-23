from datetime import datetime

from flask_login import UserMixin, AnonymousUserMixin
from sqlalchemy.ext.hybrid import hybrid_property
from werkzeug.security import generate_password_hash, check_password_hash

from .. import db
from ..utils import ModelMixin
from sqlalchemy.sql import func, expression

class User(db.Model, UserMixin, ModelMixin):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.Date, server_default=func.now())
    is_active = db.Column(db.Boolean, server_default=expression.true())
    is_superadmin = db.Column(db.Boolean, server_default=expression.false())

    @hybrid_property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    @classmethod
    def authenticate(cls, user_id, password):
        user = cls.query.filter(cls.username == user_id).first()
        if user is not None and user.is_active == True and check_password_hash(user.password, password):
            return user

    def __str__(self):
        return '<User: %s>' % self.username


class AnonymousUser(AnonymousUserMixin):
    pass

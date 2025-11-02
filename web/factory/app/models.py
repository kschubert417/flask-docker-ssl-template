from uuid6 import uuid7
from . import db
from app import db
from app import login
from flask_login import UserMixin
from flask import url_for #, current_app
from werkzeug.security import generate_password_hash, check_password_hash

def generate_uuid():
    return str(uuid7())

@login.user_loader
def load_user(id):
    # print(f"User ID: {id}")
    # return db.session.get(User, int(id))
    return db.session.get(User, id)

class PaginagedAPIMixin(object):
    @staticmethod
    def paginate_query(query, page, per_page, endpoint, **kwargs):
        # scalars = db.session.execute(query).scalars()
        resources = db.paginate(query, page=page, per_page=per_page, error_out=False)
        data = {
            'items': [item.to_dict() for item in resources.items],
            '_meta': {
                'page': page,
                'per_page': per_page,
                'total_pages': resources.pages,
                'total_items': resources.total
            },
            '_links': {
                'self': url_for(endpoint, page=page, per_page=per_page,
                                **kwargs),
                'next': url_for(endpoint, page=page + 1, per_page=per_page,
                                **kwargs) if resources.has_next else None,
                'prev': url_for(endpoint, page=page - 1, per_page=per_page,
                                **kwargs) if resources.has_prev else None
            }
        }
        return data

#class AdminUser(UserMixin, db.Model):
class User(UserMixin, db.Model):
    __tablename__ = 'admin_users'

    # id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid, unique=True, nullable=False)
    email = db.Column("email", db.String(50))
    password_hash = db.Column("password_hash", db.String(300))
    role = db.Column("role", db.String(20), default='user')
    first_name = db.Column("first_name", db.String(25))
    last_name = db.Column("last_name", db.String(25))

    # Timestamps
    createdate = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    lastlogindate = db.Column(db.DateTime(timezone=True))
    updatedate = db.Column(db.DateTime(timezone=True), onupdate=db.func.now())

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, password)

#class AdminMessages(PaginagedAPIMixin, db.Model):
class Messages(PaginagedAPIMixin, db.Model):
    __tablename__ = 'admin_messages'

    # id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid, unique=True, nullable=False)
    first_name = db.Column("first_name", db.String(50))
    last_name = db.Column("last_name", db.String(50))
    company = db.Column("company", db.String(100))
    email = db.Column("email", db.String(100))
    message = db.Column("message", db.String(1000))
    date = db.Column("date", db.Date)

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "company": self.company,
            "email": self.email,
            "message": self.message,
            "date": self.date.isoformat() if self.date else None
        }

from app import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, index=True, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password = db.Column(db.String(128))
    realname = db.Column(db.String(64))
    job = db.Column(db.String(64))
    Phone = db.Column(db.String(64))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    @property
    def password(self):
        raise AttributeError('password is not a readable attr')
    
    @password.setter
    def password(self, pwd):
        self.password = generate_password_hash(pwd, salt_length=16)

    def verify_password(self, pwd):
        return check_password_hash(self.password, pwd)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
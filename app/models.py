from app import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class Permissions(db.Model):
    __tablename__ = 'permissions'

    id = db.Column(db.Integer, index=True, primary_key=True)    


class Roles(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, index=True, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name


class Users(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(64))
    name = db.Column(db.String(64))
    job = db.Column(db.String(64))
    email = db.Column(db.String(64))
    phone = db.Column(db.String(64))
    apikey = db.Column(db.String(64))
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
    
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


class Projects(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    repo_url = db.Column(db.String(128))
    checkout_dir = db.Column(db.String(128))
    deploy_dir = db.Column(db.String(128))
    compile_cmd = db.Column(db.String(512))
    playbook_path = db.Column(db.String(128))
    created_at = db.Column(db.Integer)
    updated_at = db.Column(db.Integer)


class Hosts(db.Model):
    __tablename__ = 'hosts'

    id = db.Column(db.Integer, primary_key=True)
    hostname = db.Column(db.String(64))
    ip_address = db.Column(db.String(64), index=True, unique=True)
    ssh_port = db.Column(db.Integer)
    username = db.Column(db.String(32))
    password = db.Column(db.String(128))
    ssh_method = db.Column(db.Integer)
    project_id = db.Column(db.Integer)
    created_at = db.Column(db.Integer)
    updated_at = db.Column(db.Integer)
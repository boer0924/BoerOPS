from app import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class Permission(db.Model):
    __tablename__ = 'permissions'

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
    phone = db.Column(db.String(64))
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

class Project(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    git_repo = db.Column(db.String(128))
    checkout_dir = db.Column(db.String(128))
    deploy_dir = db.Column(db.String(128))
    compile_cmd = db.Column(db.String(512))
    playbook_file_path = db.Column(db.String(128))
    created_at = db.Column(db.Integer)
    updated_at = db.Column(db.Integer)


class Host(db.Model):
    __tablename__ = 'hosts'

    id = db.Column(db.Integer, primary_key=True)
    hostname = db.Column(db.String(64), index=True, unique=True)
    ip_address = db.Column(db.String(128))
    ssh_port = db.Column(db.String(128))
    ssh_user = db.Column(db.String(128))
    compile_cmd = db.Column(db.String(512))
    playbook_file_path = db.Column(db.String(128))
    created_at = db.Column(db.Integer)
    updated_at = db.Column(db.Integer)
    project_id = db.Column(db.Integer)
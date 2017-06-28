from app import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class Permission(db.Model):
    __tablename__ = 'permissions'

    id = db.Column(db.Integer, primary_key=True)    
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    users = db.relationship('User', backref='role', lazy="dynamic")

    def __repr__(self):
        return '<%s %r>' % (self.__class__.__name__, self.name)


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(64))
    name = db.Column(db.String(64))
    # job = db.Column(db.String(64))
    email = db.Column(db.String(64))
    phone = db.Column(db.String(64))
    apikey = db.Column(db.String(64))
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
    
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    
    @password.setter
    def password(self, pwd):
        self.password_hash = generate_password_hash(pwd, salt_length=16)

    def verify_password(self, pwd):
        return check_password_hash(self.password_hash, pwd)

    def __repr__(self):
        return '<%s %r>' % (self.__class__.__name__, self.username)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

rel_host_project = db.Table(
    "rel_host_project",
    db.Column("id", db.Integer, primary_key=True),
    db.Column("host_id", db.Integer, db.ForeignKey("hosts.id")),
    db.Column("project_id", db.Integer, db.ForeignKey("projects.id")),
    db.Column("created_at", db.DateTime, default=db.func.now()),
    db.Column("updated_at", db.DateTime, default=db.func.now(), onupdate=db.func.now()),
)


class Project(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    repo_url = db.Column(db.String(128))
    checkout_dir = db.Column(db.String(128))
    compile_dir = db.Column(db.String(128))
    compile_cmd = db.Column(db.String(512))
    playbook_path = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
    
    hosts = db.relationship("Host", secondary=rel_host_project, 
                            backref=db.backref("projects", lazy="dynamic"))

    def __repr__(self):
        return '<%s %r>' % (self.__class__.__name__, self.name)


class Host(db.Model):
    __tablename__ = 'hosts'

    id = db.Column(db.Integer, primary_key=True)
    hostname = db.Column(db.String(64))
    ip_address = db.Column(db.String(64), unique=True)
    ssh_port = db.Column(db.Integer)
    username = db.Column(db.String(32))
    password = db.Column(db.String(128))
    ssh_method = db.Column(db.Integer)
    environ = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    def __repr__(self):
        return '<%s %r>' % (self.__class__.__name__, self.ip_address)

class Deploy(db.Model):
    __tablename__ = 'deploys'

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    version = db.Column(db.String(64))
    mode = db.Column(db.Integer)
    status = db.Column(db.Integer)
    comment = db.Column(db.Text)
    result = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    user = db.relationship('User',
                           backref=db.backref("deploys", lazy="dynamic"))
    project = db.relationship('Project',
                              backref=db.backref("deploys", lazy="dynamic"))

    def __repr__(self):
        return '<%s %r>' % (self.__class__.__name__, self.version)
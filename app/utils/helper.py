# -*- coding: utf-8 -*-

from functools import wraps
from flask import g, request, redirect, url_for, json, abort, jsonify
import jwt

from app.services.users import users
from app.services.roles import roles

__all__ = [
    'get_dynamic_inventory', 'login_required', 'permission_required',
    'write_required'
]

def get_dynamic_inventory(proj, environ):
    return {
        proj.name: {
            'hosts': [{
                'hostname': h.ip_address,
                'port': h.ssh_port,
                'username': h.username,
                'password': h.password
            } for h in proj.hosts if h.environ == int(environ)],
            'vars': {
                'ansible_user': 'boer',
                'ansible_become': True,
                'ansible_become_method': 'sudo',
                'ansible_become_user': 'root',
                'ansible_become_pass': 'Admin@123'
            }
        }
    }


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.cookies.get('token')
        if not token:
            return redirect(url_for('auth.login', redirect_uri=request.path))
        try:
            token = jwt.decode(token, 'balabala')
            g.user = users.get(token['uid'])
            g.role = roles.get(token['rid'])
        except jwt.ExpiredSignature as e:
            return redirect(url_for('auth.login', redirect_uri=request.path))
        return f(*args, **kwargs)
    return decorated_function


def permission_required(*roles, alls=False):
    # http://flask.pocoo.org/snippets/98/
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if g.role.id not in roles:
                if alls:
                    abort(403)
                if request.method == 'POST':
                    return jsonify(code=405, msg='权限不足')                    
            return f(*args, **kwargs)
        return wrapped
    return wrapper


def write_required(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        if request.method == 'POST':
            return jsonify(code=405, msg='权限不足')
        return f(*args, **kwargs)
    return wrapped
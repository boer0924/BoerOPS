# -*- coding: utf-8 -*-

from functools import wraps
from flask import g, request, redirect, url_for, json
import jwt

from app.services.users import users
from app.services.roles import roles

__all__ = ['get_dynamic_inventory', 'login_required']

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


def permission_required(f):
    # http://flask.pocoo.org/snippets/98/
    pass
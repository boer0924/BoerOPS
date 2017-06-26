from . import auth
from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import login_required, login_user
import jwt

from app.services.roles import roles
from app.services.users import users

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        _u = users.first(username=username)
        if _u and _u.verify_password(password):
            resp = jsonify(code=200, msg='登录成功')
            payload = dict(
                rid = _u.role_id,
                uid = _u.id
            )
            token = jwt.encode(payload, 'balabala', algorithm='HS256')
            resp.set_cookie('token', token)
            return resp
        else:
            return jsonify(code=500, msg='用户名或密码错误')
    return render_template('auth/login.html')


@auth.route('/users', methods=['GET', 'POST'])
def user():
    token = request.cookies.get('token')
    if token:
        print(jwt.decode(token, verify=False))
    if request.method == 'POST':
        print(request.form.to_dict())
        users.create(**request.form.to_dict())
        return jsonify(code=200, msg='添加成功')
    _users = users.all()
    _roles = roles.all()
    return render_template('auth/users.html', users=_users, roles=_roles)


@auth.route('/groups', methods=['GET', 'POST'])
def group():
    if request.method == 'POST':
        roles.create(**request.form.to_dict())
        return jsonify(code=200, msg='添加成功')
    _roles = roles.all()
    return render_template('auth/groups.html', roles=_roles)

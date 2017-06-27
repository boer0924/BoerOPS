# -*- coding: utf-8 -*-

import datetime

from . import auth
from flask import render_template, flash, redirect, url_for, request, jsonify, g, make_response
import jwt

from app.services.roles import roles
from app.services.users import users
from app.utils.helper import login_required

@auth.route('/login', methods=['GET', 'POST'])
def login():
    redirect_uri = request.args.get('redirect_uri') or '/dashboard'
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        redirect_uri = request.form.get('redirect_uri')
        _u = users.first(username=username)
        if _u and _u.verify_password(password):
            resp = jsonify(code=200, msg='登录成功', redirect_uri=redirect_uri)
            payload = dict(
                exp = datetime.datetime.utcnow() + datetime.timedelta(hours=1),
                rid = _u.role_id,
                uid = _u.id
            )
            token = jwt.encode(payload, 'balabala', algorithm='HS256')
            resp.set_cookie('token', token)
            return resp
        else:
            return jsonify(code=500, msg='用户名或密码错误')
    return render_template('auth/login.html', redirect_uri=redirect_uri)


@auth.route('/users', methods=['GET', 'POST'])
@login_required
def user():
    if request.method == 'POST':
        users.create(**request.form.to_dict())
        return jsonify(code=200, msg='添加成功')
    _users = users.all()
    _roles = roles.all()
    return render_template('auth/users.html', users=_users, roles=_roles)


@auth.route('/groups', methods=['GET', 'POST'])
@login_required
def group():
    if request.method == 'POST':
        roles.create(**request.form.to_dict())
        return jsonify(code=200, msg='添加成功')
    _roles = roles.all()
    return render_template('auth/groups.html', roles=_roles)

@auth.route('/logout')
@login_required
def logout():
    resp = make_response(redirect(url_for('.login')))
    resp.set_cookie('token', '', expires=0)
    return resp

@auth.route('/reset', methods=['POST'])
@login_required
def reset_password():
    if request.method == 'POST':
        current_pass = request.form.get('current_pwd')
        new_pass = request.form.get('new_pwd')
        if g.user and g.user.verify_password(current_pass):
            g.user.password = new_pass
            users.session_commit()
            return jsonify(code=200, msg='修改成功')
        else:
            return jsonify(code=403, msg='权限不足')
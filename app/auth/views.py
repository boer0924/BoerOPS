# -*- coding: utf-8 -*-

import datetime
import json

from . import auth
from flask import render_template, redirect, url_for, request, jsonify, g, make_response, current_app
import jwt

from app.services.roles import roles
from app.services.users import users
from app.utils.helper import login_required, permission_required, write_required
from app import redis

@auth.route('/login', methods=['GET', 'POST'])
def login():
    redirect_uri = request.args.get('redirect_uri') or '/dashboard'
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        redirect_uri = request.form.get('redirect_uri')
        _u = users.first(username=username)
        if _u and _u.verify_password(password):
            # 获取缓存，动态设置config
            role_map = redis.get('roles').decode('utf-8')
            current_app.config['roles'] = json.loads(role_map)
            # 处理登录、生成token
            resp = jsonify(code=200, msg='登录成功', redirect_uri=redirect_uri)
            payload = dict(
                exp = datetime.datetime.utcnow() + datetime.timedelta(hours=8),
                rid = _u.role_id,
                uid = _u.id
            )
            token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')
            resp.set_cookie('token', token)
            return resp
        else:
            return jsonify(code=500, msg='用户名或密码错误')
    return render_template('auth/login.html', redirect_uri=redirect_uri)


@auth.route('/users', methods=['GET', 'POST'])
@login_required
@permission_required(3)
def user():
    if request.method == 'POST':
        users.create(**request.form.to_dict())
        return jsonify(code=200, msg='添加成功')
    _users = users.all()
    _roles = roles.all()
    return render_template('auth/users.html', users=_users, roles=_roles)


@auth.route('/groups', methods=['GET', 'POST'])
@login_required
@permission_required(3, alls=True)
def group():
    if request.method == 'POST':
        roles.create(**request.form.to_dict())
        # 每次添加角色，更新redis roles
        all_roles = roles.all()
        all_role_ids = map(lambda x: x.id, all_roles)
        all_role_names = map(lambda x: x.name, all_roles)  
        role_map = dict(zip(all_role_names, all_role_ids))
        redis.set('roles', json.dumps(role_map))
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


@auth.route('/test')
def test_for_someting():
    print(current_app.config['roles'].get('测试'))
    return ''


@auth.errorhandler(403)
def access_forbidden(e):
    return render_template('auth/403.html'), 403
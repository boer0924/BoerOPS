from . import auth
from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import login_required, login_user

from app.services.roles import roles
from app.services.users import users

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        _u = users.first(username=username)
        if _u.verify_password(password):
            return jsonify(code=200, msg='登录成功')
    return render_template('auth/login.html')

@auth.route('/users', methods=['GET', 'POST'])
def user():
    if request.method == 'POST':
        role = request.get('job')
    _users = users.all()
    return render_template('auth/users.html', users=_users)


@auth.route('/groups', methods=['GET', 'POST'])
def group():
    if request.method == 'POST':
        roles.create(**request.form.to_dict())
        return jsonify(code=200, msg='添加成功')
    _roles = roles.all()
    return render_template('auth/groups.html', roles=_roles)

@auth.route('/reg', methods=['GET', 'POST'])
def reg():
    role = request.args.get('role')
    print('====>', role)
    if role:
        roles.create(name=role)
    print(roles.all())
    return 'done'
    # return render_template('auth/registry.html')

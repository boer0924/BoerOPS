from . import auth
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required, login_user

from app.services.roles import roles
from app.services.users import users

@auth.route('/login')
def login():
    return render_template('auth/login.html')

@auth.route('/user')
def user():
    return render_template('auth/index.html')


@auth.route('/reg', methods=['GET', 'POST'])
def reg():
    role = request.args.get('role')
    print('====>', role)
    if role:
        roles.create(name=role)
    print(roles.all())
    return 'done'
    # return render_template('auth/registry.html')

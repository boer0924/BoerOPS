from . import auth
from flask import render_template, flash, redirect, url_for
from flask_login import login_required, login_user

@auth.route('/login')
def login():
    return render_template('auth/login.html')

@auth.route('/user')
def user():
    return render_template('auth/user.html')


@auth.route('/reg', methods=['GET', 'POST'])
def user_add():
    return render_template('auth/registry.html')

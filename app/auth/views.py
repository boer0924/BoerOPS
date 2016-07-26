from . import auth
from flask import render_template
from .forms import LoginForm, RegistryForm

@auth.route('/user')
def user():
    return render_template('auth/user.html')


@auth.route('/user/add', methods=['GET', 'POST'])
def user_add():
    form = RegistryForm()
    return render_template('auth/registry.html', form=form)

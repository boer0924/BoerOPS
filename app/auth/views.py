from . import auth
from flask import render_template

@auth.route('/user')
def user():
    return render_template('user.html')
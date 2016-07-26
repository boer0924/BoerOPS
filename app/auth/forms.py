from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import Email, EqualTo, DataRequired

class LoginForm(Form):
    username = StringField('username', [DataRequired()])
    password = PasswordField('password', [DataRequired()])
    remember = BooleanField('remember', default=False)


class RegistryForm(Form):
    username = StringField('username', [DataRequired()])
    email = StringField('email', [Email()])
    password = PasswordField('password', [DataRequired()])
    confirm = PasswordField('confirm', [EqualTo(password, message='Confirm password must match')])
    name = StringField('name', [DataRequired()])
    job = StringField('job')
    phone = StringField('phone')

from flask_wtf import Form
from wtforms import StringField,SelectField
from wtforms.validators import DataRequired


class ProjectForm(Form):
    name = StringField('name', [DataRequired()])
    git_url = StringField('git_url', [DataRequired()])
    git_path = StringField('git_path', [DataRequired()])
    build_path = StringField('build_path', [DataRequired()])
    package_path = StringField('package_path', [DataRequired()])
    prod_path = StringField('prod_path', [DataRequired()])


class DeployForm(Form):
    project = SelectField('project', [DataRequired()])
    branch = StringField('branch')


class RollbackForm(Form):
    project = SelectField('project', [DataRequired()])
    commit = StringField('commit id', [DataRequired()])

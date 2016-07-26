from . import main
from flask import render_template
from .forms import ProjectForm, DeployForm, RollbackForm


@main.route('/')
def index():
    return render_template('main/index.html')


@main.route('/deploy')
def deploy():
    form = DeployForm()
    form.project.choices = []
    return render_template('main/deploy.html', form=form)


@main.route('/rollback')
def rollback():
    form = RollbackForm()
    form.project.choices = []
    return render_template('main/project/rollback.html', form=form)


@main.route('/project')
def project():
    return render_template('main/project/project.html')


@main.route('/project/add', methods=['GET', 'POST'])
def project_add():
    form = ProjectForm()
    return render_template('main/project/add.html', form=form)

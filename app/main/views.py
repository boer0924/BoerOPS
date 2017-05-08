from . import main
from flask import render_template


@main.route('/')
def index():
    # return render_template('main/index.html')
    return render_template('base.html')


@main.route('/deploy')
def deploy():
    return render_template('main/deploy.html')


@main.route('/rollback')
def rollback():
    return render_template('main/project/rollback.html')


@main.route('/project')
def project():
    return render_template('main/project/project.html')


@main.route('/project/create', methods=['GET', 'POST'])
def create_project():
    return render_template('main/project/create.html')

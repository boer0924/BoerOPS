from . import projects
from flask import render_template, request, jsonify


@projects.route('/', methods=['POST'])
def upload():
    if request.method == 'POST':
        return jsonify(filepath='/var/www/v3.yml')


@projects.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        print(request.values)
        # print(request.form.get('playbook'))
    return render_template('projects/index.html')

@projects.route('/hosts', methods=['GET', 'POST'])
def hosts():
    if request.method == 'POST':
        print(request.form)
        print(request.form.get('hostname'))
    return render_template('projects/hosts.html')


@projects.route('/deploy')
def deploy():
    return render_template('projects/deploy.html')


@projects.route('/rollback')
def rollback():
    return render_template('projects/rollback.html')


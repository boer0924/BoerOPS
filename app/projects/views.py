#!/usr/local/env python
# -*- coding: utf-8 -*-

from . import projects
from ..utils.uploads import upload_file
from ..models import db, Projects, Hosts

from flask import render_template, request, jsonify, current_app

@projects.route('/uploads', methods=['GET', 'POST'])
def uploads():
    return upload_file()

@projects.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form.get('name')
        repo_url = request.form.get('gitrepo')
        checkout_dir = request.form.get('checkoutdir')
        deploy_dir = request.form.get('deploydir')
        compile_cmd = request.form.get('compilecmd')
        playbook_path = request.form.get('file')
    
        _p = Projects(
            name = name,
            repo_url = repo_url,
            checkout_dir = checkout_dir,
            deploy_dir = deploy_dir,
            compile_cmd = compile_cmd,
            playbook_path = playbook_path,
            created_at = int(time.time()),
            updated_at = int(time.time())
        )
        db.session.add(_p)
        db.session.commit()

    return render_template('projects/index.html')

@projects.route('/hosts', methods=['GET', 'POST'])
def hosts():
    if request.method == 'POST':
        print(request.form)
        print(request.form.get('hostname'))
    return render_template('projects/hosts.html')


@projects.route('/deploy')
def deploy():
    print('------>', current_app.root_path)
    return render_template('projects/deploy.html')


@projects.route('/rollback')
def rollback():
    return render_template('projects/rollback.html')


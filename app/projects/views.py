#!/usr/local/env python
# -*- coding: utf-8 -*-

from . import projects
from app.utils.uploads import upload_file
from app.services.projects import projs
from app.services.hosts import hosts

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


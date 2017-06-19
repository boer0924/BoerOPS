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

@projects.route('/bind', methods=['POST'])
def binds():
    _hosts = request.form
    print(_hosts)
    _hosts = request.form.getlist('hosts[]')
    print(_hosts)
    return 'done'

@projects.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        _id = request.form.get('id')
        name = request.form.get('name')
        repo_url = request.form.get('repo_url')
        checkout_dir = request.form.get('checkout_dir')
        compile_dir = request.form.get('compile_dir')
        compile_cmd = request.form.get('compile_cmd')
        playbook_path = request.form.get('playbook_path')

        fields = dict(
            name = name,
            repo_url = repo_url,
            checkout_dir = checkout_dir,
            compile_dir = compile_dir,
            compile_cmd = compile_cmd,
            playbook_path = playbook_path
        )
        # 修改操作
        if _id is not None:
            proj = projs.first(id=_id)
            if not proj:
                return jsonify(code=404, msg='记录不存在')
            
            try:
                projs.update(proj, **fields)
            except Exception as e:
                return jsonify(code=500, msg='修改失败')     
            return jsonify(code=200, msg='修改成功')
                       
        # 添加操作
        try:
            projs.create(**fields)
        except Exception as e:
            print(e)
            return jsonify(code=500, msg='添加失败')
        return jsonify(code=200, msg='添加成功')
    
    _projects = projs.all()
    _hosts = hosts.all()
    return render_template('projects/index.html', projects=_projects, hosts=_hosts)

@projects.route('/hosts', methods=['GET', 'POST'])
def project_hosts():
    if request.method == 'POST':
        _id = request.form.get('id')
        # 修改操作
        if _id is not None:
            host = hosts.first(id=_id)
            if not host:
                return jsonify(code=404, msg='记录不存在')
            
            try:
                hosts.update(host, **request.form.to_dict())
            except Exception as e:
                return jsonify(code=500, msg='修改失败')     
            return jsonify(code=200, msg='修改成功')
                       
        # 添加操作
        try:
            hosts.create(**request.form.to_dict())
        except Exception as e:
            print(e)
            return jsonify(code=500, msg='添加失败')
        return jsonify(code=200, msg='添加成功')
    _hosts = hosts.all()
    return render_template('projects/hosts.html', hosts=_hosts)


@projects.route('/deploy')
def deploy():
    return render_template('projects/deploy.html')


@projects.route('/rollback')
def rollback():
    return render_template('projects/rollback.html')


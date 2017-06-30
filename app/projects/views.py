#!/usr/local/env python
# -*- coding: utf-8 -*-

from . import projects
from app.utils.uploads import upload_file
from app.utils.remoteshell import MyRunner
from app.utils.helper import get_dynamic_inventory, login_required
from app.services.projects import projs
from app.services.hosts import hosts
from app.services.deploys import deploys

from flask import render_template, request, jsonify, current_app, g

import os

@projects.route('/uploads', methods=['GET', 'POST'])
@login_required
def uploads():
    UPLOAD_FOLDER = os.path.join(os.path.dirname(current_app.root_path), 'playbook')
    return upload_file(UPLOAD_FOLDER)

@projects.route('/bind', methods=['POST'])
@login_required
def binds():
    _project_id = request.form.get('project_id')
    _hosts = request.form.getlist('hosts[]')
    proj = projs.get(_project_id)
    for host in set(_hosts):
        proj.hosts.append(hosts.get(int(host)))
    projs.save(proj)
    return jsonify(code=200, msg='绑定成功')

@projects.route('/', methods=['GET', 'POST'])
@login_required
def index():
    if request.method == 'POST':
        _id = request.form.get('id')
        fields = request.form.to_dict()
        fields.pop('playbook')
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
@login_required
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


@projects.route('/deploy', methods=['GET', 'POST'])
@login_required
def deploy_step_first():
    if request.method == 'POST':
        fields = request.form.to_dict()
        project_name = fields.get('name')
        version = fields.get('version')
        environ = fields.get('environ')
        proj = projs.first(name=project_name.strip())
        if not proj:
            return jsonify(rc=400, msg='项目不存在')
        if int(environ) == 2:
            num_deploy = deploys.count(project_id=proj.id, status=3)            
            if int(num_deploy) >= 1:
                return jsonify(code=500, msg='有其他任务在上线中...')
            deploys.create(
                project_id=proj.id,
                user_id=g.user.id,
                version=version,
                mode=environ,
                status=3)
        else:
            num_deploy = deploys.count(project_id=proj.id, status=0)
            if int(num_deploy) >= 1:
                return jsonify(code=500, msg='有其他任务在提测中...')
            deploys.create(
                project_id=proj.id,
                user_id=g.user.id,
                version=version,
                mode=environ)
        results = deploys.deploy_task(proj.id, int(environ))
        print(results)
        return jsonify(code=200, msg='job done', status=results)
    return render_template('projects/deploy.html')


@projects.route('/deploy/second', methods=['GET', 'POST'])
@login_required
def deploy_step_second():
    if request.method == 'POST':

        results = deploys.deploy_task(proj.id)
        return jsonify(code=200, msg='job done', status=status)


@projects.route('/rollback')
def rollback():
    return render_template('projects/rollback.html')

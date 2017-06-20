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
    _project_id = request.form.get('project_id')
    _hosts = request.form.getlist('hosts[]')
    proj = projs.get(_project_id)
    for host in set(_hosts):
        proj.hosts.append(hosts.get(int(host)))
    projs.save(proj)
    return jsonify(code=200, msg='绑定成功')

@projects.route('/', methods=['GET', 'POST'])
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
    for p in _projects:
        # 测试主机
        proj_test_hosts = [h.ip_address for h in p.hosts if h.environ == 0]
        # 生产主机
        proj_prod_hosts = [h.ip_address for h in p.hosts if h.environ == 1]
        print(proj_test_hosts, proj_prod_hosts)
        print('-----------')
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


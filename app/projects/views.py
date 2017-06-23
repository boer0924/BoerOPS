#!/usr/local/env python
# -*- coding: utf-8 -*-

from . import projects
from app.utils.uploads import upload_file
from app.utils.remoteshell import MyRunner
from app.utils.helper import get_dynamic_inventory
from app.services.projects import projs
from app.services.hosts import hosts
from app.services.deploys import deploys

from flask import render_template, request, jsonify, current_app

import os

@projects.route('/uploads', methods=['GET', 'POST'])
def uploads():
    UPLOAD_FOLDER = os.path.join(os.path.dirname(current_app.root_path), 'playbook')
    return upload_file(UPLOAD_FOLDER)

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
    # for index, p in enumerate(_projects):
        # host_lists = [h.ip_address for h in p.hosts if h.environ == 2]
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


@projects.route('/deploy', methods=['GET', 'POST'])
def deploy():
    # 全部项目列表
    # ps = map(lambda p: p.name, projs.all())
    # all_projects = list(ps)
    if request.method == 'POST':
        fields = request.form.to_dict()
        project_name = fields.get('name')
        version = fields.get('version')
        environ = fields.get('environ')        

        proj = projs.first(name=project_name.strip())
        if not proj:
            return jsonify(rc=400, msg='项目不存在')
        
        import os
        import subprocess
        cmd = 'git clone -q %s %s' % (proj.repo_url, proj.checkout_dir)
        
        git_path = os.path.join(proj.checkout_dir, '.git')
        if os.path.exists(git_path) and os.path.isdir(git_path):
            cmd = 'cd %s && git fetch --all -fq' % proj.checkout_dir
        rc = subprocess.call(cmd, shell=True)
        if rc != 0:
            return jsonify(code=500, msg='获取代码失败')
        cmd = 'cd %s && git reset -q --hard %s' % (proj.checkout_dir, version.strip())
        rc = subprocess.call(cmd, shell=True)
        print('----reset-----', cmd)
        if rc != 0:
            return jsonify(code=500, msg='检出代码失败')
        cmd = 'rsync -qa --delete --exclude .git %s%s %s%s' % (proj.checkout_dir, os.sep, proj.compile_dir, os.sep)
        rc = subprocess.call(cmd, shell=True)
        print('---rsync-----', cmd)
        if rc != 0:
            return jsonify(code=500, msg='同步代码失败')
        user_cmds = proj.compile_cmd.split('\n')
        print('--list---', user_cmds)
        user_cmds = ' && '.join(user_cmds)
        print('--string---', user_cmds)
        rc = subprocess.call(user_cmds, shell=True)
        if rc != 0:
            return jsonify(code=500, msg='用户命令执行失败')
        resource = get_dynamic_inventory(proj, environ)
        # print(resource)
        host_lists = [h.ip_address for h in proj.hosts if h.environ == int(environ)]
        runner = MyRunner(resource)
        # ansible playbook
        runner.run_playbook(host_lists, proj.playbook_path)
        print(runner.get_playbook_result())
        print('\n-----\n')
        runner.run_module(host_lists, 'shell', 'whoami')
        print(runner.get_module_result())
        return jsonify(code=200, msg='job done')

        # subprocess.check_call()
        # subprocess.check_output()

    return render_template('projects/deploy.html')


@projects.route('/rollback')
def rollback():
    return render_template('projects/rollback.html')

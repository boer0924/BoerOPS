#!/usr/local/env python
# -*- coding: utf-8 -*-

from . import projects
from app.utils.uploads import upload_file
from app.services.projects import projs
from app.services.hosts import hosts
from app.services.deploys import deploys

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
        proj_30test_hosts = [h.ip_address for h in p.hosts if h.environ == 0]
        proj_31test_hosts = [h.ip_address for h in p.hosts if h.environ == 1]
        # 生产主机
        proj_prod_hosts = [h.ip_address for h in p.hosts if h.environ == 2]
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
        
        # hosts_list = [{'hostname': h.ip_address, 'port': h.ssh_port, 'username': h.username, 'password': h.password} for h in proj.hosts if h.environ == int(environ)]

        import subprocess
        cmd = 'git clone -q %s %s' % (proj.repo_url, proj.checkout_dir)
        rc = subprocess.call(cmd, shell=True)
        if rc != 0:
            jsonify()

        subprocess.check_call()
        subprocess.check_output()

        resource = {
            proj.name: {
                'hosts': [{'hostname': h.ip_address, 'port': h.ssh_port, 'username': h.username, 'password': h.password} for h in proj.hosts if h.environ == int(environ)]
            }
        }
        print(resource)

    return render_template('projects/deploy.html')


@projects.route('/rollback')
def rollback():
    return render_template('projects/rollback.html')


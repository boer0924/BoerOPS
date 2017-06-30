#!/usr/local/env python
# -*- coding: utf-8 -*-

import os
import subprocess

from flask import g

from . import Base
from app.models import Deploy
from app.utils.remoteshell import MyRunner
from app.utils.helper import get_dynamic_inventory

class DeployService(Base):
    __model__ = Deploy

    def deploy_task(self, project_id, environ):
        c_d = self.first(project_id=project_id, status=0) if int(environ) != 2 else self.first(project_id=project_id, status=3)
        if not c_d:
            return
        # 检出代码库
        cmd = 'git clone -q %s %s' % (c_d.project.repo_url, c_d.project.checkout_dir)
        git_path = os.path.join(c_d.project.checkout_dir, '.git')
        if os.path.exists(git_path) and os.path.isdir(git_path):
            cmd = 'cd %s && git fetch --all -fq' % c_d.project.checkout_dir
        rc = subprocess.call(cmd, shell=True)
        # 指定版本
        cmd = 'cd %s && git reset -q --hard %s' % (c_d.project.checkout_dir, c_d.version.strip())
        rc = subprocess.call(cmd, shell=True)
        # 同步到编译/打包目录
        cmd = 'rsync -qa --delete --exclude .git %s%s %s%s' % (c_d.project.checkout_dir, os.sep, c_d.project.compile_dir, os.sep)
        rc = subprocess.call(cmd, shell=True)
        # 执行用户自定义命令（权限，fis编译，打包）
        cmds = c_d.project.compile_cmd.split('\n')
        cmds = ' && '.join(cmds)
        rc = subprocess.call(cmds, shell=True)
        # 获取ansible动态Inventory
        resource = get_dynamic_inventory(c_d.project, environ)
        host_lists = [h.ip_address for h in c_d.project.hosts if h.environ == int(environ)]
        # 执行ansible playbook
        runner = MyRunner(resource)
        runner.run_playbook(host_lists, c_d.project.playbook_path)
        if int(environ) == 2:
            self.update(c_d, status=4)
        else:
            self.update(c_d, status=1)
        # return runner.get_playbook_result()
        return self.get(id=c_d.id).status

    
    def rollback(self, deploy):
        pass

deploys = DeployService()
# -*- coding: utf-8 -*-
import os
import shutil
import subprocess
import json
from threading import Thread

from flask import Flask, request, render_template
from flask_mail import Mail, Message

app = Flask(__name__)

mail = Mail(app)

app.config['MAIL_SERVER'] = 'mail.heclouds.com'
app.config['MAIL_PORT'] = 25
app.config['MAIL_USERNAME'] = 'boer'
app.config['MAIL_PASSWORD'] = '123456'

app.config['CHECKOUT_DIR'] = '/data/deployment/gitrepos'
app.config['DEPLOY_DIR'] = '/data/deployment/deploydir'
app.config['PROJECTS_DIR'] = '/data/deployment/projects'

def update_repo(repo_path, repo_url, commit_id):
    git_path = os.path.join(repo_path, '.git')
    if os.path.exists(git_path) and os.path.isdir(git_path):
        cmd = 'git reset --hard origin/master && git pull -q'
        rc = subprocess.check_call(cmd.split(), cwd=repo_path)
    else:
        if os.path.exists(repo_path):
            shutil.rmtree(repo_path)
        os.makedirs(os.path.dirname(repo_path))
        cmd = 'git clone -q %s' % repo_url
        rc = subprocess.check_call(cmd.split(), cwd=os.path.dirname(repo_path))
    # 指定commit_id
    cmd = 'git reset -q --hard %s' % commit_id
    rc = subprocess.check_call(cmd.split(), cwd=repo_path)
    
def rsync_local(src, dest, excludes=[]):
    excludes.append('.git')
    exclude_args = ''
    for e in excludes:
        exclude_args = exclude_args + ' --exclude %s' % e
    cmd = 'rsync -qa --delete %s %s%s %s%s' % (exclude_args, src, os.sep, dest, os.sep)
    rc = subprocess.check_call(cmd.split(), cwd=repo_path)

def chk_and_set_exe(src_path):
    if not os.access(src_path, os.X_OK):
        os.chmod(src_path, 755)

# 同步邮件
def send_email(sender, to, cc, subject, template, **kwargs):
    msg = Message(subject, sender=sender, recipients=to, cc=cc)
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    mail.send(msg)

# 异步发邮件
def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(sender, to, cc, subject, template, **kwargs):
    msg = Message(subject, sender=sender, recipients=to, cc=cc)
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr   

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        results = json.loads(request.data)
        # user 相关
        name = results['user']['name']
        username = results['user']['username']
        # repository 相关
        repo_name = results['repository']['name']
        repo_url = results['repository']['url']
        repo_path = git_path = os.path.join(app.config['CHECKOUT_DIR'], repo_name, repo_name)
        # commit 相关
        commit_id = results['commit']['id']
        commit_msg = results['commit']['message'].strip('\n')
        # object_attributes 相关
        noteable_type = results['object_attributes']['noteable_type']
        # Triggered when a new comment is made on commits, merge requests, issues, and code snippets. 
        if noteable_type != 'Commit':
            return ''
        try:
            notes = results['object_attributes']['note']
            if not notes.startswith('```json') and not notes.endswith('```'):
                return ''
            notes = notes.lstrip('```json').rstrip('```').replace('\r\n', '') 
            notes = json.loads(notes)
        except Exception as e:
            print('<-debug->', e)
            # send_email()
            return ''
        deploy_type = notes.get('deploy_type')
        recipients = notes.get('recipients')
        carbon_copy = notes.get('carbon_copy')
        functions = notes.get('functions')

        update_repo(repo_path, repo_url, commit_id)
        rsync_local(repo_path, os.path.join(app.config['DEPLOY_DIR'], repo_name, repo_name))
        
        script_file = os.path.join(app.config['PROJECTS_DIR'], repo_name, 'script/local_before.sh')
        if deploy_type == 'weekfix':
            pass
        elif deploy_type == 'hotfix':
            pass
        elif deploy_type == 'feature':
            pass
        elif deploy_type == 'prod':
            pass
        else:
            print('滚蛋吧')
        if os.path.exists(script_file) and os.path.isfile(script_file):
            chk_and_set_exe(script_file)
            output = subprocess.check_output(script_file)
            print(output)
        return ''
    return ''

if __name__ == '__main__':
    app.run(host='172.19.3.23', port=8080)
# {
#     "deploy_type": "weekfix/feature/hotfix/prod",
#     "recipients": ["mazhijie", "limao", "dengdeng"],
#     "carbon_copy": ["bmwlee", "limao"],
#     "functions": [
#         {
#             "name": "功能点一",
#             "content": "balabala~"
#         },
#         {
#             "name": "功能点二",
#             "content": "balabala~"
#         }
#     ]
# }

# onenet_v3
# onenet_ee
# forum_v2
# passport
# phpcorelib
# groupservice
# admin_onenetv3
# campaignmap
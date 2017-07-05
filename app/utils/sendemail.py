MAIL_SERVER = 'mail.heclouds.com'
MAIL_PORT = 25
MAIL_USERNAME = 'boer'
MAIL_PASSWORD = '123456'

from flask import render_template
from flask_mail import Mail, Message

mail = Mail(app)

sender = ''
subject = ''
to = []

def send_email(sender, to, cc, subject, template, **kwargs):
    msg = Message(subject, sender=sender, recipients=to, cc=cc)
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    mail.send(msg)

# 异步发邮件
from threading import Thread

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

# 
from flask import Flask, request

import json

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        results = json.loads(request.data)
        # user 相关
        name = results['user']['name']
        username = results['user']['username']
        # repository 项目
        repo_name = results['repository']['name']
        repo_url = results['repository']['url']
        # commit 相关
        commit_id = results['commit']['id']
        commit_msg = results['commit']['message'].strip('\n')
        try:
            notes = json.loads(results['object_attributes']['note'].strip('\r\n'))
        except ValueError as e:
            print(e) # app.logger
            # send_email()
            return ''
        deploy_type = notes['deploy_type'].encode('utf-8')
        
        return ''
    return ''


if __name__ == '__main__':
    app.run(host='172.19.3.23', port=8080)
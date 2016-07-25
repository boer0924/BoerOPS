from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/deploy')
def deploy():
    return render_template('deploy.html')

@app.route('/project')
def project():
    return render_template('project.html')

@app.route('/user')
def user():
    return render_template('user.html')
# -*- coding: utf-8 -*-
from . import main
from flask import render_template, redirect
from app.utils.helper import login_required
from app.services.deploys import deploys

@main.route('/')
def index():
    return redirect('/dashboard')


@main.route('/dashboard')
@login_required
def dashboard():
    u_ds = deploys.find(status=5)
    return render_template('main/index.html')
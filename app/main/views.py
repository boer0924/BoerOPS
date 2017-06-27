# -*- coding: utf-8 -*-
from . import main
from flask import render_template, redirect


@main.route('/')
def index():
    return redirect('/dashboard')


@main.route('/dashboard')
def dashboard():
    return render_template('main/index.html')
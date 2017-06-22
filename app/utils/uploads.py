# -*- coding: utf-8 -*-
"""文件上传"""

import os

from flask import request, current_app, jsonify
from werkzeug.utils import secure_filename


# UPLOAD_FOLDER = os.path.join(os.path.dirname(current_app.root_path), 'playbook')
# UPLOAD_FOLDER = os.path.join(os.path.dirname(current_app.root_path), 'playbook')
ALLOWED_EXTENSIONS = set(['yml', 'yaml', 'txt'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def gen_file_name(filename):
    flag = 1
    while os.path.exists(os.path.join(UPLOAD_FOLDER, filename)):
        name, ext = os.path.splitext(filename)
        filename = '%s_%s%s' % (name, str(flag), ext)
        flag += 1
    return filename

def upload_file(UPLOAD_FOLDER):
    if request.method == 'POST':
        file = request.files.get('playbook')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            uploaded_file_path = os.path.join(UPLOAD_FOLDER, filename)
            if not os.path.exists(os.path.dirname(uploaded_file_path)):
                try:
                    os.makedirs(os.path.dirname(uploaded_file_path))
                except OSError as e:
                    return jsonify(rc=0)
            file.save(uploaded_file_path)
            return jsonify(rc=1, filepath=uploaded_file_path)
        else:
            return jsonify(rc=0)

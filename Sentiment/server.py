# -*- coding: utf-8 -*-
from flask import Flask, render_template, redirect, url_for, make_response, request
import os
app = Flask(__name__)
app.debug = True

"""
@app.route('/')
def hello_world():
    return 'Hello World!'
"""

@app.route('/')
def hello_world():
    return redirect('/home')

@app.route('/home')
def home():
    status = request.cookies.get('_file_status')
    if status != 'ok':
        return render_template('home.html', _sample_number=None, status="no_file")
    else:
        _sample_num = request.cookies.get('_sample_number')
        _file_name = request.cookies.get('filename')
        return render_template('home.html', _sample_number = _sample_num, status="ok", _info="上传成功", filename=_file_name)


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    # only the POST request is allowed
    if request.method == 'POST':
        file = request.files['file']
        if file:
            if file.filename.endswith('.txt'):
                file.save(os.path.join(os.getcwd(), file.filename))
                fp = open(file.filename)
                _sample_number = 0
                for line in fp:
                    if line.strip('\n').strip(' ') == '':
                        # blank line will be ignored
                        continue
                    _sample_number += 1
                fp.close()
                if _sample_number == 0:
                    return render_template('home.html', _sample_number = 1111111, status="empty_file", _info="数据文件为空, 请重新上传")
                resp = make_response(redirect(url_for('home')))
                resp.set_cookie('_file_status', "ok")
                resp.set_cookie('_sample_number', '%s' % _sample_number)
                resp.set_cookie('filename', file.filename)
                return resp
            else:
                return render_template('home.html', _sample_number = 1111111, status="format_error", _info="文件格式错误, 请重新上传")

@app.route('/description')
def description():
    return render_template('description.html')

@app.route('/evaluation')
def evaluation():
    return render_template('evaluations.html')

@app.route('/information')
def info():
    return render_template('details.html')

@app.route('/delete_file')
def del_file():
    resp = make_response(redirect(url_for('home')))
    resp.set_cookie('_file_status', '', expires=0)
    resp.set_cookie('_sample_number', '', expires=0)
    resp.set_cookie('filename', '', expires=0)
    return resp

if __name__ == '__main__':
    app.run(host='0.0.0.0')

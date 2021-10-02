# coding=GBK
from flask import Flask, redirect, url_for, render_template, request

app = Flask(__name__)


@app.route('/hello/<name>')
def hello_world(name):
    if name == 'admin':
        return redirect(url_for('print_song'))
    else:
        return 'Welcome! %s' % name


@app.route('/table/')
def table1():
    return render_template('table.html')


@app.route('/result', methods=['POST', 'GET'])
def result():
    if request.method == 'POST':
        result = request.form
        return render_template('result.html', result=result)


@app.route('/admin/')
def print_song():
    return render_template('fan.html')


@app.route('/')
def print_fan():
    # 传入数据
    my_str = 'welcome!'
    my_dict = {'name': 'admin', 'num': 1}
    return render_template('hello.html',
                           my_dict=my_dict,
                           my_str=my_str)


if __name__ == '__main__':
    app.run('0.0.0.0', 800, debug=True)

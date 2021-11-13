from flask import Flask, request
from flask import render_template
from flask import jsonify
import pandas as pd                         #导入pandas包
import utils
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/index')
def hello_index():
    return render_template("index.html")


@app.route('/data')
def get_data():
    data = utils.get_data()
    return utils.get_data()


@app.route('/time')
def get_time():
    return utils.get_time()


@app.route('/baidu')
def hello_baidu():
    return render_template("baidu.html")


if __name__ == '__main__':
    app.run()

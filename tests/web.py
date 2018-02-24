# !/usr/bin/env python
# -*- encoding: utf-8 -*-
# vim: set et sw=4 ts=4 sts=4 ff=unix fenc=utf8:
# Author: Vincent<vincent8280@outlook.com>
#         http://wax8280.github.io
# Created on 2018/2/24 9:32
from flask import Flask, abort

app = Flask(__name__)


@app.route('/hello_world')
def hello_world():
    return 'Hello World!'


@app.route('/retry_delay')
def retry_delay():
    abort(401)


if __name__ == '__main__':
    app.run()

# !/usr/bin/env python
# -*- encoding: utf-8 -*-
# vim: set et sw=4 ts=4 sts=4 ff=unix fenc=utf8:
# Author: Vincent<vincent8280@outlook.com>
#         http://wax8280.github.io
# Created on 2018/1/1 12:30
import json
import os
import sys
import multiprocessing
from copy import deepcopy
from flask import render_template, Response, Flask, request, make_response

from web2kindle.libs.utils import write_config, load_config
from web2kindle.script import SCRIPTS, SCRIPT_CONFIGS, SCRIPT_FUNC

app = Flask(__name__)
app.debug = False

# 打包成exe，必须更改目录
if getattr(sys, 'frozen', False):
    multiprocessing.freeze_support()
    template_folder = os.path.join(sys.executable, '..', 'webui', 'templates')
    static_folder = os.path.join(sys.executable, '..', 'webui', 'static')
    app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)


@app.route('/')
def index_page():
    return render_template('index.html', scripts=SCRIPTS)


@app.route('/config', methods=['POST', 'GET'])
def config_page():
    config_path = './web2kindle/config'
    configs = deepcopy(SCRIPT_CONFIGS)

    if request.method == 'GET':
        # 加载默认值
        for each_script in configs:
            path = os.path.join(config_path, each_script['script_name'] + '.yml')
            a = load_config(path)
            for config_name, config_value in a.items():
                for each_config in each_script['configs']:
                    if each_config['config_name'] == config_name:
                        each_config['value'] = config_value
        return render_template('config.html', configs=configs)
    elif request.method == 'POST':
        new_config = {}

        form_data = request.form.to_dict()
        for k, v in form_data.items():
            if '_check' in k:
                new_config[k.replace('_check', '')] = form_data[k.replace('_check', '')]

        write_config(os.path.join(config_path, form_data['script_name'] + '.yml'), new_config)
        return Response()


@app.route('/doc')
def doc_page():
    return render_template('doc.html')


@app.route('/guide_cli')
def guide_cli_page():
    return render_template('guide_cli.html')


@app.route('/guide_gui')
def guide_gui_page():
    return render_template('guide_gui.html')


@app.route('/action', methods=['POST'])
def action():
    form_data = request.form.to_dict()
    script_name = form_data['script_name']
    form_data.pop('script_name')
    form_data.setdefault('img', False)
    form_data.setdefault('gif', False)
    form_data.setdefault('email', False)

    kw = {}
    for k, v in form_data.items():
        if k == 'img' or k == 'gif' or k == 'email':
            if v is not False:
                v = True
        if v != '' and v != 'kw':
            kw.setdefault(k, v)

    if form_data['kw']:
        try:
            data = json.loads(form_data['kw'])
        except Exception:
            import traceback
            traceback.print_exc()
            return make_response("无法解析'参数'数据，请确保格式正确")
        kw.update(data)

    SCRIPT_FUNC[script_name](**kw)
    return make_response()


if __name__ == '__main__':
    from web2kindle import load_config, MAIN_CONFIG

    print("""                                                                                                         
                      VVV         VVVVVV   VVV          VVV                     VVV    VVV               
                      VVV        VVVVVVVV  VVV          VVV                     VVV    VVV               
                      VVV        VVV  VVVV VVV                                  VVV    VVV               
                      VVV       VVV    VVV VVV                                  VVV    VVV               
                      VVV             VVVV VVV                                  VVV    VVV               
 VVVVVVVVVVV VVVVVVV  VVVVVVVV        VVV  VVV  VVVV    VVV     VVVVVVVV   VVVVVVVV    VVV      VVVVVV   
 VVVVVVVVVV VVVV VVVV VVVV VVVV      VVVV  VVV VVV      VVV     VVVV VVVV VVVV VVVV    VVV     VVV  VVV  
 VVVVVVVVVV VVV   VVV VVVV  VVV      VVV   VVVVVV       VVV     VVV   VVV VVV  VVVV    VVV    VVVV  VVVV 
 VVVVVVVVVV VVVVVVVVV VVV   VVVV    VVV    VVVVVV       VVV     VVV   VVVVVVV   VVV    VVV    VVVVVVVVVV 
  VVVVVVVVV VVV       VVV   VVVV   VVVV    VVVVVVV      VVV     VVV   VVVVVVV   VVV    VVV    VVV        
  VVVVVVVV  VVV       VVV   VVV   VVVV     VVV VVV      VVV     VVV   VVV VVV   VVV    VVV    VVVV       
  VVVVVVVV  VVVV  VVV VVVV  VVV  VVVV      VVV  VVV     VVV     VVV   VVV VVV  VVVV    VVV     VVV  VVVV 
  VVVV VVV   VVVVVVVV VVVVVVVVV  VVVVVVVVV VVV  VVVV    VVV     VVV   VVV VVVVVVVVV    VVV     VVVVVVVV  
   VVV VVV    VVVVV   VVVVVVV    VVVVVVVVV VVV   VVV    VVV     VVV   VVV   VVVVVVV    VVV       VVVVV   
                                                                                                         
---------------------------------------------------------------------------------------------------------
Author:wax8280
Email:wax8280@163.com
Github:github.com/wax8280/web2kindle
Version:1.0.0.0""")
    app.run(port=MAIN_CONFIG.get('WEBUI_PORT', 1101))

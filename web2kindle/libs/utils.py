# !/usr/bin/env python
# -*- encoding: utf-8 -*-
# vim: set et sw=4 ts=4 sts=4 ff=unix fenc=utf8:
# Author: Vincent<vincent8280@outlook.com>
#         http://wax8280.github.io
# Created on 2017/10/10 9:52
import heapq
import os
import random
import re
import yaml
import hashlib
import platform

from functools import wraps


def md5string(x):
    return hashlib.md5(x.encode()).hexdigest()


def singleton(cls):
    instances = {}

    @wraps(cls)
    def getinstance(*args, **kw):
        if cls not in instances:
            the_instances = cls(*args, **kw)
            instances[cls] = the_instances
            return the_instances
        else:
            return instances[cls]

    return getinstance


def load_config(path):
    try:
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return yaml.load(f)
        except UnicodeDecodeError:
            with open(path, 'r') as f:
                return yaml.load(f)
    except FileNotFoundError:
        return {}


def write_config(path, d):
    # path所在的目录
    if not os.path.exists(os.path.split(path)[0]):
        os.makedirs((os.path.split(path)[0]))

    dump_string = yaml.dump(d)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(dump_string)


def get_system():
    return platform.system()


def find_file(rootdir, pattern):
    finded = []
    for i in os.listdir(rootdir):
        if not os.path.isdir(os.path.join(rootdir, i)):
            if re.search(pattern, i):
                finded.append(os.path.join(rootdir, i))
    return finded


def write(folder_path, file_path, content, mode='wb'):
    path = os.path.join(folder_path, file_path)
    if not os.path.exists(os.path.split(path)[0]):
        try:
            os.makedirs((os.path.split(path)[0]))
        except FileExistsError:
            pass
    with open(path, mode) as f:
        f.write(content)


def codes_write(folder_path, file_path, content, mode='wb'):
    path = os.path.join(folder_path, file_path)
    if not os.path.exists(os.path.split(path)[0]):
        os.makedirs((os.path.split(path)[0]))
    with open(path, mode) as f:
        f.write(content)


def format_file_name(file_name, a=''):
    file_name = re.sub(r'[ \\/:*?"<>→|+]', '', file_name)

    if a:
        # 文件名太长无法保存mobi
        if len(file_name) + len(a) + 2 > 55:
            _ = 55 - len(a) - 2 - 3
            file_name = file_name[:_] + '...（{}）'.format(a)
        else:
            file_name = file_name + '（{}）'.format(a)
    else:
        if len(file_name) > 55:
            _ = 55 - 3
            file_name = file_name[:_] + '...'
        else:
            file_name = file_name
    return file_name


def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
    return str(text)


def read_file_to_list(path):
    try:
        with open(path, 'r') as f:
            return [i.strip() for i in list(f.readlines())]
    except FileNotFoundError as e:
        return str(e)
    except Exception as e:
        return str(e)


def check_config(main_config, script_config, config_name, logger):
    if config_name not in script_config:
        if config_name in main_config:
            script_config.update({config_name: main_config.get(config_name)})
        else:
            logger.log_it("在配置文件中没有发现'{}'项，请确认主配置文件中或脚本配置文件中存在该项。".format(config_name), 'ERROR')
            os._exit(0)


def split_list(the_list, window):
    return [the_list[i:i + window] for i in range(0, len(the_list), window)]


def random_char(c):
    return [chr(random.choice(list(set(range(65, 123)) - set(range(91, 97))))) for i in range(c)]


class PriorityList(list):
    """
    >>> a = PriorityList()
    >>> a.priority_push([150, ['t5', 't6']])
    >>> print(a)
    [[150, ['t5', 't6']]]
    >>> a.priority_push([50, ['t1', 't2']])
    >>> print(a)
    [[50, ['t1', 't2']], [150, ['t5', 't6']]]
    >>> a.priority_push([100, ['t3', 't4']])
    >>> print(a)
    [[50, ['t1', 't2']], [150, ['t5', 't6']], [100, ['t3', 't4']]]
    >>> print(a.priority_pop())
    [50, ['t1', 't2']]
    >>> print(a)
    [[100, ['t3', 't4']], [150, ['t5', 't6']]]
    """

    def priority_pop(self):
        # lowest is first
        try:
            return heapq.heappop(self)
        except IndexError:
            return None

    def priority_push(self, item):
        heapq.heappush(self, item)

# !/usr/bin/env python
# -*- encoding: utf-8 -*-
# vim: set et sw=4 ts=4 sts=4 ff=unix fenc=utf8:
# Author: Vincent<vincent8280@outlook.com>
#         http://wax8280.github.io
# Created on 2017/10/10 9:52
import datetime
import os
import random
import re
import yaml
import hashlib
import platform
import time

from functools import wraps


def md5string(x: str) -> str:
    return hashlib.md5(x.encode()).hexdigest()


def singleton(cls):
    """ 单例模式，用于装饰类 """
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


def load_config(path: str) -> dict:
    """ 读取yml配置文件 """
    try:
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return yaml.load(f)
        except UnicodeDecodeError:
            with open(path, 'r') as f:
                return yaml.load(f)
    except FileNotFoundError:
        return {}


def write_config(path: str, d: dict) -> None:
    """ 写yml配置文件 """
    # path所在的目录
    if not os.path.exists(os.path.split(path)[0]):
        os.makedirs((os.path.split(path)[0]))

    dump_string = yaml.dump(d)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(dump_string)


def get_system() -> str:
    return platform.system()


def find_file(rootdir: str, pattern: str) -> list:
    """ 用正则表达式寻找文件 """
    finded = []
    for i in os.listdir(rootdir):
        if not os.path.isdir(os.path.join(rootdir, i)):
            if re.search(pattern, i):
                finded.append(os.path.join(rootdir, i))
    return finded


def write(folder_path: str, file_name: str, content: str, mode: str = 'wb') -> None:
    path = os.path.join(folder_path, file_name)
    if not os.path.exists(os.path.split(path)[0]):
        os.makedirs((os.path.split(path)[0]))
    with open(path, mode) as f:
        f.write(content)


def format_file_name(file_name: str, a: str = '') -> str:
    """格式化文件名（去除文件名的一些特殊字符，同一长度等）"""
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


def read_file(path: str, encode: str = 'utf-8') -> str:
    with open(path, 'r', encoding=encode) as f:
        text = f.read()
    return str(text)


def read_file_to_list(path: str) -> list or str:
    try:
        with open(path, 'r') as f:
            return [i.strip() for i in list(f.readlines())]
    except FileNotFoundError as e:
        return str(e)
    except Exception as e:
        return str(e)


def check_config(main_config: dict, script_config: dict, config_name: str, logger) -> None:
    if config_name not in script_config:
        if config_name in main_config:
            script_config.update({config_name: main_config.get(config_name)})
        else:
            logger.log_it("在配置文件中没有发现'{}'项，请确认主配置文件中或脚本配置文件中存在该项。".format(config_name), 'ERROR')
            os._exit(0)


def split_list(the_list: list, window: int) -> list:
    """ 将the_list分割成子list，每个子list有window项 """
    return [the_list[i:i + window] for i in range(0, len(the_list), window)]


def random_char(c: int) -> list:
    """ 返回c个随机字符 """
    return [chr(random.choice(list(set(range(65, 123)) - set(range(91, 97))))) for i in range(c)]


def get_next_datetime_string(data_string: str, format_string: str, days: int, prev=False) -> str:
    now_datatime = datetime.datetime.strptime(data_string, format_string)
    if prev:
        return (now_datatime - datetime.timedelta(days=days)).strftime(format_string)
    else:
        return (now_datatime + datetime.timedelta(days=days)).strftime(format_string)


def compare_datetime_string(data_stringA: str, data_stringB: str, format_string: str) -> bool:
    """return true if data_stringA is bigger"""
    return datetime.datetime.strptime(data_stringA, format_string) > datetime.datetime.strptime(data_stringB,
                                                                                                format_string)


def get_datetime_string(format_string: str) -> str:
    return datetime.datetime.fromtimestamp(time.time()).strftime(format_string)

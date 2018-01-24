# !/usr/bin/env python
# -*- encoding: utf-8 -*-
# vim: set et sw=4 ts=4 sts=4 ff=unix fenc=utf8:
# Author: Vincent<vincent8280@outlook.com>
#         http://wax8280.github.io
# Created on 2017/10/10 9:53
from web2kindle.libs.utils import read_file_to_list

INF = 999999999


def zhihu_collection_main(i, f=None, start=1, end=INF, img=True, gif=False, email=False, **kw):
    import web2kindle.script.zhihu_collection

    kw.update({
        'img': img,
        'gif': gif,
        'email': email,
    })
    if i:
        web2kindle.script.zhihu_collection.main([i], int(start), int(end), kw)
    elif f:
        collection_list = read_file_to_list(f)
        if not isinstance(collection_list, list):
            collection_list = [collection_list]
        web2kindle.script.zhihu_collection.main(collection_list, start, end, kw)


def zhihu_zhuanlan_main(i, f=None, start=1, end=INF, img=True, gif=False, email=False, **kw):
    import web2kindle.script.zhihu_zhuanlan

    kw.update({
        'img': img,
        'gif': gif,
        'email': email,
    })

    if i:
        web2kindle.script.zhihu_zhuanlan.main([i], int(start), int(end), kw)
    elif f:
        zhuanlan_list = read_file_to_list(f)
        if not isinstance(zhuanlan_list, list):
            zhuanlan_list = [zhuanlan_list]
        web2kindle.script.zhihu_zhuanlan.main(zhuanlan_list, start, end, kw)


def zhihu_answers_main(i, f=None, start=1, end=INF, img=True, gif=False, email=False, **kw):
    import web2kindle.script.zhihu_answers

    kw.update({
        'img': img,
        'gif': gif,
        'email': email,
    })

    if i:
        web2kindle.script.zhihu_answers.main([i], int(start), int(end), kw)
    elif f:
        people_list = read_file_to_list(f)
        if not isinstance(people_list, list):
            people_list = [people_list]
        web2kindle.script.zhihu_answers.main(people_list, start, end, kw)


def guoke_scientific_main(start=0, end=INF, img=True, gif=False, email=False, **kw):
    import web2kindle.script.guoke_scientific

    kw.update({
        'img': img,
        'gif': gif,
        'email': email,
    })
    web2kindle.script.guoke_scientific.main(int(start), int(end), kw)


def qdaily_main(start='default', end='default', i='home', img=True, gif=False, email=False, **kw):
    import web2kindle.script.qdaily, datetime, time

    kw.update({
        'img': img,
        'gif': gif,
        'type': i,
        'email': email,
    })
    if start == 'default':
        start = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d')
    if end == 'default':
        end = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d')

    web2kindle.script.qdaily.main(start, end, kw)


def jianshu_wenji_main(i, f=None, start=1, end=INF, img=True, gif=False, email=False, **kw):
    import web2kindle.script.jianshu_wenji

    kw.update({
        'img': img,
        'gif': gif,
        'email': email,
    })

    if i:
        web2kindle.script.jianshu_wenji.main([i], int(start), int(end), kw)
    elif f:
        l = read_file_to_list(f)
        if not isinstance(l, list):
            l = [l]
        web2kindle.script.jianshu_wenji.main(l, start, end, kw)


def jianshu_zhuanti_main(i, f=None, start=1, end=INF, img=True, gif=False, email=False, **kw):
    import web2kindle.script.jianshu_zhuanti
    
    kw.update({
        'img': img,
        'gif': gif,
        'email': email,
    })

    if i:
        web2kindle.script.jianshu_zhuanti.main([i], int(start), int(end), kw)
    elif f:
        l = read_file_to_list(f)
        if not isinstance(l, list):
            l = [l]
        web2kindle.script.jianshu_zhuanti.main(l, start, end, kw)


def jianshu_user_main(i, f=None, start=1, end=INF, img=True, gif=False, email=False, **kw):
    import web2kindle.script.jianshu_user

    kw.update({
        'img': img,
        'gif': gif,
        'email': email,
    })

    if i:
        web2kindle.script.jianshu_user.main([i], int(start), int(end), kw)
    elif f:
        l = read_file_to_list(f)
        if not isinstance(l, list):
            l = [l]
        web2kindle.script.jianshu_user.main(l, start, end, kw)


def make_mobi(path, window=50, multi=True):
    from web2kindle.libs.db import ArticleDB
    from web2kindle import MAIN_CONFIG
    from web2kindle.libs.html2kindle import HTML2Kindle

    if not path:
        import os
        path = os.getcwd()

    items = []
    with ArticleDB(path) as db:
        db.reset_version()
        items.extend(db.select_article())
        book_name = db.select_meta('BOOK_NAME')

    if items:
        with HTML2Kindle(items, path, book_name, MAIN_CONFIG.get('KINDLEGEN_PATH')) as html2kindle:
            html2kindle.make_metadata(window)
            if multi:
                html2kindle.make_book_multi(path)
            else:
                html2kindle.make_book(path)


def send_mobi(path):
    if not path:
        import os
        path = os.getcwd()

    from web2kindle.libs.send_email import SendEmail2Kindle
    with SendEmail2Kindle() as s:
        s.send_all_mobi(path)


SCRIPTS = [{'script_name': 'zhihu_collection',
            'script_introduction': '获取知乎收藏夹',
            'i': (True, '收藏夹编号'),
            'start': True,
            'img': True,
            'gif': True,
            'email': True, },
           {'script_name': 'zhihu_answers',
            'script_introduction': '获取知乎答主',
            'i': (True, '答主名称'),
            'start': True,
            'img': True,
            'gif': True,
            'email': True, },
           {'script_name': 'zhihu_zhuanlan',
            'script_introduction': '获取知乎专栏',
            'i': (True, '专栏名称'),
            'start': True,
            'img': True,
            'gif': True,
            'email': True, },
           {'script_name': 'guoke_scientific',
            'script_introduction': '获取果壳网科学人',
            'i': False,
            'start': True,
            'img': True,
            'gif': True,
            'email': True, },
           {'script_name': 'qdaily',
            'script_introduction': '获取好奇心日报',
            'i': (True, '获取类型'),
            'start': True,
            'img': True,
            'gif': True,
            'email': True, },
           {'script_name': 'jianshu_wenji',
            'script_introduction': '获取简书文集',
            'i': (True, '文集ID'),
            'start': True,
            'img': True,
            'gif': True,
            'email': True, },
           {'script_name': 'jianshu_zhuanti',
            'script_introduction': '获取简书专题',
            'i': (True, '专题ID'),
            'start': True,
            'img': True,
            'gif': True,
            'email': True, },
           {'script_name': 'jianshu_user',
            'script_introduction': '获取简书用户文章',
            'i': (True, '用户ID'),
            'start': True,
            'img': True,
            'gif': True,
            'email': True, },
           ]

SCRIPT_FUNC = {
    'zhihu_collection': zhihu_collection_main,
    'zhihu_zhuanlan': zhihu_zhuanlan_main,
    'zhihu_answers': zhihu_answers_main,
    'guoke_scientific': guoke_scientific_main,
    'qdaily': qdaily_main,
    'jianshu_wenji': jianshu_wenji_main,
    'jianshu_zhuanti': jianshu_zhuanti_main,
    'jianshu_user': jianshu_user_main,
}

SCRIPT_CONFIGS = [
    {
        'script_name': 'config',
        'configs': [
            {
                'config_name': 'KINDLEGEN_PATH',
                'config_introduction': "KindleGen.exe程序所在路径",
                'requried': False,
                'default': '',
            },
            {
                'config_name': 'SAVE_PATH',
                'config_introduction': "全局保存路径。优先使用各个脚本独立的SAVE_PATH",
                'requried': True,
                'default': '',
            },
            {
                'config_name': 'LOG_PATH',
                'config_introduction': "日志文件的路径",
                'requried': False,
                'default': '',
            },
            {
                'config_name': 'LOG_LEVEL',
                'config_introduction': "日志等级",
                'requried': False,
                'default': 'INFO',
            },
            {
                'config_name': 'WRITE_LOG',
                'config_introduction': "是否写日志文件，默认否",
                'requried': False,
                'default': False,
            },
            {
                'config_name': 'DOWNLOADER_WORKER',
                'config_introduction': "启动Downloader的数量，数量越多下载速度越快。建议为1~3。默认为1",
                'requried': False,
                'default': 1,
            },
            {
                'config_name': 'PARSER_WORKER',
                'config_introduction': "启动Parser的数量。建议为1。默认为1",
                'requried': False,
                'default': 1,
            },
            {
                'config_name': 'RESULTER_WORKER',
                'config_introduction': "Resulter。建议为1。默认为1",
                'requried': False,
                'default': 1,
            },
            {
                'config_name': 'EMAIL_USERNAME',
                'config_introduction': "发送给Kindle的邮箱地址",
                'requried': False,
                'default': '',
            },
            {
                'config_name': 'PASSWORD',
                'config_introduction': "发送给Kindle的邮箱密码",
                'requried': False,
                'default': '',
            },
            {
                'config_name': 'SMTP_ADDR',
                'config_introduction': "发送给Kindle的邮箱SMTP。一般，163邮箱的为`smtp.163.com`；QQ邮箱为`smtp.qq.com`。",
                'requried': False,
                'default': '',
            },
            {
                'config_name': 'KINDLE_ADDR',
                'config_introduction': "Kindle接受推送的邮箱",
                'requried': False,
                'default': '',
            },

        ]
    },
    {
        'script_name': 'zhihu_collection',
        'configs': [{
            'config_name': 'SAVE_PATH',
            'config_introduction': "保存路径名",
            'default': '',
            'requried': False
        }]
    },
    {
        'script_name': 'zhihu_zhuanlan',
        'configs': [{
            'config_name': 'SAVE_PATH',
            'config_introduction': "保存路径名",
            'default': '',
            'requried': False
        }]
    },
    {
        'script_name': 'zhihu_answers',
        'configs': [{
            'config_name': 'SAVE_PATH',
            'config_introduction': "保存路径名",
            'default': '',
            'requried': False
        }]
    },
    {
        'script_name': 'guoke_scientific',
        'configs': [{
            'config_name': 'SAVE_PATH',
            'config_introduction': "保存路径名",
            'default': '',
            'requried': False
        }]
    },
    {
        'script_name': 'qdaily',
        'configs': [{
            'config_name': 'SAVE_PATH',
            'config_introduction': "保存路径名",
            'default': '',
            'requried': False
        }]
    },
    {
        'script_name': 'jianshu_wenji',
        'configs': [{
            'config_name': 'SAVE_PATH',
            'config_introduction': "保存路径名",
            'default': '',
            'requried': False
        }]
    },
    {
        'script_name': 'jianshu_zhuanti',
        'configs': [{
            'config_name': 'SAVE_PATH',
            'config_introduction': "保存路径名",
            'default': '',
            'requried': False
        }]
    },
    {
        'script_name': 'jianshu_user',
        'configs': [{
            'config_name': 'SAVE_PATH',
            'config_introduction': "保存路径名",
            'default': '',
            'requried': False
        }]
    },

]

# !/usr/bin/env python
# -*- encoding: utf-8 -*-
# vim: set et sw=4 ts=4 sts=4 ff=unix fenc=utf8:
# Author: Vincent<vincent8280@outlook.com>
#         http://wax8280.github.io
# Created on 2017/10/10 9:53
from web2kindle.libs.utils import read_file_to_list


def zhihu_collection_main(i, f=None, start=1, end=999999, img=True, gif=False, email=False):
    import web2kindle.script.zhihu_collection
    kw = {}
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


def zhihu_zhuanlan_main(i, f=None, start=1, end=999999, img=True, gif=False, email=False):
    import web2kindle.script.zhihu_zhuanlan
    kw = {}
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


def zhihu_answers_main(i, f=None, start=1, end=999999, img=True, gif=False, email=False):
    import web2kindle.script.zhihu_answers
    kw = {}
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


def guoke_scientific_main(start=0, end=999999, img=True, gif=False, email=False):
    import web2kindle.script.guoke_scientific
    kw = {}
    kw.update({
        'img': img,
        'gif': gif,
        'email': email,
    })
    web2kindle.script.guoke_scientific.main(int(start), int(end), kw)


def qdaily_main(start='default', end='default', i='home', img=True, gif=False, email=False):
    import web2kindle.script.qdaily, datetime, time
    kw = {}
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

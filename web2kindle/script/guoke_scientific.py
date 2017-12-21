# !/usr/bin/env python
# -*- encoding: utf-8 -*-
# vim: set et sw=4 ts=4 sts=4 ff=unix fenc=utf8:
# Author: Vincent<vincent8280@outlook.com>
#         http://wax8280.github.io
# Created on 17-10-23 下午7:14
import os
import re
import time
from copy import deepcopy
from queue import Queue, PriorityQueue
from urllib.parse import urlparse
from bs4 import BeautifulSoup

from web2kindle import MAIN_CONFIG
from web2kindle.libs.crawler import Crawler, RetryDownload, Task
from web2kindle.libs.db import ArticleDB
from web2kindle.libs.html2kindle import HTML2Kindle
from web2kindle.libs.send_email import SendEmail2Kindle
from web2kindle.libs.utils import write, load_config, check_config, md5string
from web2kindle.libs.log import Log

SCRIPT_CONFIG = load_config('./web2kindle/config/guoke_scientific_config.yml')
LOG = Log("guoke_scientific")
API_URL = "http://www.guokr.com/apis/minisite/article.json?retrieve_type=by_subject&limit=20&offset={}&_=1508757235776"
DEFAULT_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/'
                  '61.0.3163.100 Safari/537.36'
}
check_config(MAIN_CONFIG, SCRIPT_CONFIG, 'SAVE_PATH', LOG)
ARTICLE_ID_SET = set()


def main(start, end, kw):
    iq = PriorityQueue()
    oq = PriorityQueue()
    result_q = Queue()
    crawler = Crawler(iq, oq, result_q, MAIN_CONFIG.get('PARSER_WORKER', 1), MAIN_CONFIG.get('DOWNLOADER_WORKER', 1),
                      MAIN_CONFIG.get('RESULTER_WORKER', 1))
    new = True

    default_headers = deepcopy(DEFAULT_HEADERS)
    default_headers.update({'Referer': 'http://www.guokr.com/scientific/'})
    save_path = SCRIPT_CONFIG['SAVE_PATH']
    book_name = '果壳网'
    task = Task.make_task({
        'url': API_URL.format(start),
        'method': 'GET',
        'meta': {'headers': default_headers, 'verify': False},
        'parser': parser_list,
        'priority': 0,
        'save': {
            'cursor': start,
            'start': start,
            'end': end,
            'kw': kw,
            'save_path': SCRIPT_CONFIG['SAVE_PATH'],
        },
        'retry': 3,
    })
    iq.put(task)
    # Init DB
    with ArticleDB(save_path, VERSION=0) as db:
        _ = db.select_all_article_id()
    if _:
        for each in _:
            ARTICLE_ID_SET.add(each[0])

    crawler.start()

    items = []
    with ArticleDB(save_path) as db:
        items.extend(db.select_article())
        db.insert_meta_data(['BOOK_NAME', book_name])
        db.increase_version()

    if items:
        new = True
        with HTML2Kindle(items, save_path, book_name, MAIN_CONFIG.get('KINDLEGEN_PATH')) as html2kindle:
            html2kindle.make_metadata(window=kw.get('window', 50))
            html2kindle.make_book_multi(save_path)
    else:
        LOG.log_it('无新项目', 'INFO')
        new = False

    if new and kw.get('email'):
        with SendEmail2Kindle() as s:
            s.send_all_mobi(SCRIPT_CONFIG['SAVE_PATH'])
    os._exit(0)


def parser_list(task):
    response = task['response']
    new_tasks = []
    to_next = True

    if not response:
        LOG.log_it("Not Response", 'WARN')
        raise RetryDownload

    try:
        data = response.json()
    except Exception as e:
        LOG.log_it('解析JSON出错（如一直出现，而且浏览器能正常访问，可能是网站代码升级，请通知开发者。）\nERRINFO:{}'
                   .format(str(e)), 'WARN')
        raise RetryDownload

    try:
        for each_result in data['result']:
            url = each_result['url']
            article_id = md5string(url)
            if article_id not in ARTICLE_ID_SET:
                title = each_result['title']
                date_group = re.search('(.*?)T(.*?)\+', each_result['date_created'])
                date = date_group.group(1) + ' ' + date_group.group(2)

                meta = deepcopy(task['meta'])
                save = deepcopy(task['save'])
                save.update({
                    'title': title,
                    'date': date
                })
                new_task = Task.make_task({
                    'url': url,
                    'method': 'GET',
                    'parser': parser_content,
                    'resulter': resulter_content,
                    'priority': 1,
                    'meta': meta,
                    'save': save
                })
                new_tasks.append(new_task)
            else:
                to_next = False
    except KeyError:
        LOG.log_it('JSON KEY出错（如一直出现，而且浏览器能正常访问，可能是网站代码升级，请通知开发者。）', 'WARN')
        raise RetryDownload

    # 获取下一页
    if to_next and task['save']['cursor'] < task['save']['end'] and not len(data['result']) < 20:
        meta = deepcopy(task['meta'])
        save = deepcopy(task['save'])
        save['cursor'] += 20
        new_task = Task.make_task({
            'url': API_URL.format(save['cursor']),
            'method': 'GET',
            'meta': meta,
            'parser': parser_list,
            'priority': 0,
            'save': save,
            'retry': 3,
        })
        new_tasks.append(new_task)

    return None, new_tasks


def parser_content(task):
    response = task['response']
    if not response:
        LOG.log_it("Not Response", 'WARN')
        raise RetryDownload

    new_tasks = []
    items = []
    content = response.text
    # 去除空格
    content = content.replace('</p><p>', '').replace('<br/>', '')
    soup = BeautifulSoup(content, 'lxml')

    title = task['save']['title']
    article_url = task['url']
    created_time = soup.select('.content-th-info span')[0].string[3:]
    author = soup.select('.content-th-info a')[0].string

    download_img_list, content = format_content(soup, task)
    items.append([md5string(article_url), title, content, created_time, '', author, int(time.time() * 100000)])

    if task['save']['kw'].get('img', True):
        img_header = deepcopy(DEFAULT_HEADERS)
        img_header.update({'Referer': response.url})
        for img_url in download_img_list:
            new_tasks.append(Task.make_task({
                'url': img_url,
                'method': 'GET',
                'meta': {'headers': img_header, 'verify': False},
                'parser': parser_downloader_img,
                'resulter': resulter_downloader_img,
                'priority': 2,
                'save': task['save']
            }))
    task.update({'parsed_data': items})
    return task, new_tasks


def resulter_content(task):
    LOG.log_it("正在将任务 {} 插入数据库".format(task['tid']), 'INFO')
    with ArticleDB(task['save']['save_path']) as article_db:
        article_db.insert_article(task['parsed_data'])


def parser_downloader_img(task):
    return task, None


def resulter_downloader_img(task):
    write(os.path.join(task['save']['save_path'], 'static'), urlparse(task['response'].url).path[1:],
          task['response'].content, mode='wb')


def convert_link(x):
    return 'src="./static/{}"'.format(urlparse(x.group(1)).path[1:])


def format_content(soup, task):
    content_select = soup.select('.document')

    # 移除每页后面无用的信息
    if content_select:
        for to_del in soup.select('.copyright'):
            to_del.decompose()

    content = str(content_select)
    # bs4会自动加html和body 标签
    content = re.sub('<html><body>(.*?)</body></html>', lambda x: x.group(1), content, flags=re.S)

    # 去掉"[]"
    content = content[1:-1]

    bs2 = BeautifulSoup(content, 'lxml')
    # 居中图片
    for tab in bs2.select('img'):
        tab.wrap(bs2.new_tag('div', style='text-align:center;'))
        tab['style'] = "display: inline-block;"

        # 删除gif
        if task['save']['kw']['gif'] is False:
            if 'gif' in tab['src']:
                tab.decompose()

    content = str(bs2)
    download_img_list = (re.findall('src="(http.*?)"', content))
    # 更换为本地相对路径
    content = re.sub('src="(.*?)"', convert_link, content)
    return download_img_list, content

# !/usr/bin/env python
# -*- encoding: utf-8 -*-
# vim: set et sw=4 ts=4 sts=4 ff=unix fenc=utf8:
# Author: Vincent<vincent8280@outlook.com>
#         http://wax8280.github.io
# Created on 2018/2/24 9:13
from queue import PriorityQueue, Queue
from unittest import TestCase

import time

from web2kindle.libs.crawler import Crawler, Task, RetryDownload


class TestCrawler(TestCase):
    PARSER_WORKER = 1
    DOWNLOADER_WORKER = 1
    RESULTER_WORKER = 1

    def setUp(self):
        self.iq = PriorityQueue()
        self.oq = PriorityQueue()
        self.result_q = Queue()
        self.crawler = Crawler(self.iq, self.oq, self.result_q, TestCrawler.PARSER_WORKER,
                               TestCrawler.DOWNLOADER_WORKER, TestCrawler.RESULTER_WORKER)

    def test_normal(self):
        def parser_mock(task):
            self.assertEqual(task['response'].text, "Hello World!")
            return None, None

        task = Task.make_task({
            'url': "http://127.0.0.1:5000/hello_world",
            'method': 'GET',
            'parser': parser_mock,
            'priority': 0,
        })
        self.iq.put(task)

        self.crawler.start()

    def test_retry_delay(self):
        delay = 1
        t = time.time() - delay

        def parser_mock(task):
            nonlocal t
            self.assertTrue(time.time() - t >= delay)
            t = time.time()
            raise RetryDownload
            return None, None

        task = Task.make_task({
            'url': "http://127.0.0.1:5000/retry_delay",
            'method': 'GET',
            'parser': parser_mock,
            'priority': 0,
            'retry_delay': delay,
            'retry': 3
        })

        self.iq.put(task)

        self.crawler.start()

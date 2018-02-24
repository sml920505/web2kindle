# !/usr/bin/env python
# -*- encoding: utf-8 -*-
# vim: set et sw=4 ts=4 sts=4 ff=unix fenc=utf8:
# Author: Vincent<vincent8280@outlook.com>
#         http://wax8280.github.io
# Created on 2018/2/13 11:35
from queue import PriorityQueue
from threading import Lock, Thread
from unittest import TestCase
import random
import time

from web2kindle.libs.crawler import TaskManager, Task, COND

THREAD_WORKER = 5
SEC = 1


class TestTaskManager(TestCase):
    def setUp(self):
        super().tearDown()
        self.lock = Lock()
        self.to_download_q = PriorityQueue()
        self.task_manager = TaskManager(to_download_q=self.to_download_q)
        self.start_timestamp = self.task_manager.start_timestamp
        self.start = True

        self.count_task = 0

    def mock_downloader_to_push_in_delayqueue(self):
        def parser_mock():
            return None, None

        tasks = [Task.make_task({
            'url': 'http://www.baidu.com?a={}'.format(random.randint(1, 999)),
            'method': 'GET',
            'retry_delay': random.random() * SEC,
            'parser': parser_mock,
        }) for _ in range(20)]

        for task in tasks:
            # time.sleep(random.random())
            task['to_download_timestamp'] = time.time() + task['retry_delay']
            TaskManager.push_delay_queue(task)

    def mock_downloader_get_task_from_downloaderq(self):
        while self.start:
            try:
                t = self.to_download_q.get(timeout=1 * SEC)
            except:
                return
            # 测试误差
            # print((time.time() - t['to_download_timestamp']) / t['to_download_timestamp'])
            self.count_task += 1

    def mock_thread_wait(self):
        self.wait = True
        with COND:
            COND.wait()
        self.wait = False

    def test_retry_delay_queue(self):
        for i in range(THREAD_WORKER):
            Thread(target=self.mock_downloader_to_push_in_delayqueue).start()

        Thread(target=self.mock_thread_wait).start()

        Thread(target=self.task_manager.run).start()

        t = Thread(target=self.mock_downloader_get_task_from_downloaderq)
        t.start()
        t.join()

        self.task_manager.exit()
        # task数量正确
        self.assertEqual(self.count_task, THREAD_WORKER * 20)
        # 能够唤醒
        self.assertFalse(self.wait)

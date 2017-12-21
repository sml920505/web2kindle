# !/usr/bin/env python
# -*- encoding: utf-8 -*-
# vim: set et sw=4 ts=4 sts=4 ff=unix fenc=utf8:
# Author: Vincent<vincent8280@outlook.com>
#         http://wax8280.github.io
# Created on 17-12-13 下午9:56
import sqlite3
import os
from functools import wraps
from threading import current_thread

DB_NAME = 'article.db'

TABLE_ARTICLE_SQL = """
CREATE TABLE ARTICLE(
  ARTICLE_ID              CHAR(32) PRIMARY KEY ,
  TITLE                   TEXT ,
  CONTENT                 TEXT ,
  CONTENT_PUBLISH_TIME    TEXT ,
  VOTE_UP_COUNT           TEXT ,
  AUTHOR                  TEXT ,
  CONTENT_INSERT_TIME     INTEGER ,
  VERSION                 INTEGER,
  CONSTRAINT uc_PersonID UNIQUE (ARTICLE_ID,TITLE)
);
"""
TABLE_META_SQL = """
CREATE TABLE META(
  META                  TEXT  PRIMARY KEY ,
  DATA                  TEXT
);
"""
TABLES_SQL = [TABLE_ARTICLE_SQL, TABLE_META_SQL]

INSERT_META_DATA_SQL = "INSERT INTO META VALUES (?,?)"
UPDATE_META_DATA_SQL = "UPDATE META SET DATA = ? WHERE META = ?"

INSERT_ARTICLE_SQL = "INSERT INTO ARTICLE VALUES (?,?,?,?,?,?,?,?);"
SELECT_ARTICLE_SQL = "SELECT * FROM ARTICLE WHERE VERSION = ?"
SELECT_LAST_VERION_FROM_ARTICLE_SQL = "SELECT MAX(VERSION) FROM ARTICLE;"
SELECT_METADATA_SQL = "SELECT DATA FROM META WHERE META = ?"
SELECT_ALL_ARTICLE_ID_SQL = "SELECT ARTICLE_ID FROM ARTICLE"


def insert_meta_data_static(cursor, conn, meta_data: list, update=True):
    try:
        cursor.execute(INSERT_META_DATA_SQL, meta_data)
    except sqlite3.IntegrityError as e:
        if "UNIQUE constraint failed" in str(e) and update:
            meta_data.reverse()
            cursor.execute(UPDATE_META_DATA_SQL, meta_data)
    finally:
        conn.commit()


def On_DBCreate(cls):
    init = False
    instances_for_each_thread = {}

    @wraps(cls)
    def getinstance(*args, **kw):
        nonlocal init
        if not init:
            if 'script_save_path' in kw:
                path = kw['script_save_path']
            else:
                path = args[0]

            if not os.path.exists(path):
                try:
                    os.makedirs(path)
                except FileExistsError:
                    pass

            conn = sqlite3.connect(os.path.join(path, DB_NAME))
            cursor = conn.cursor()
            for table in TABLES_SQL:
                try:
                    cursor.execute(table)
                    conn.commit()
                except sqlite3.OperationalError as e:
                    if 'table ARTICLE already exists' in str(e):
                        pass
            for k, v in kw.items():
                insert_meta_data_static(cursor, conn, [k, v], update=False)

            init = True

        # 每一个线程公用一个实例
        thread_name = current_thread().getName()
        if cls not in instances_for_each_thread:
            instance = cls(*args, **kw)
            instances_for_each_thread[thread_name] = instance
            return instance
        else:
            return instances_for_each_thread[thread_name]

    return getinstance


@On_DBCreate
class ArticleDB:
    # FIXME:sqlite3.OperationalError: database is locked
    def __init__(self, script_save_path, **kwargs):
        self.script_save_path = script_save_path

    def __enter__(self):
        if not os.path.exists(self.script_save_path):
            os.makedirs(self.script_save_path)

        self.conn = sqlite3.connect(os.path.join(self.script_save_path, DB_NAME))
        self.cursor = self.conn.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()

    def create_table(self):
        for table in TABLES_SQL:
            try:
                self.cursor.execute(table)
                self.conn.commit()
            except sqlite3.OperationalError as e:
                if 'table ARTICLE already exists' in str(e):
                    pass

    def select_version(self):
        return int(self.select_meta('VERSION'))

    def increase_version(self):
        version = self.select_version()
        self.insert_meta_data(['VERSION', version + 1])

    def insert_meta_data(self, meta_data: list, update=True):
        insert_meta_data_static(self.cursor, self.conn, meta_data, update)

    def insert_article(self, items):
        if not len(items):
            return

        # 这次插入的VERSION比上次大
        last_version = self.select_version()
        if not isinstance(items[0], list):
            items = [items]
        if last_version is None:
            new_version = 1
        else:
            new_version = last_version + 1

        for item in items:
            item.append(new_version)
            try:
                # 忽略ARTICLE_ID(由url得到的md5)重复的
                self.cursor.execute(INSERT_ARTICLE_SQL, item)
            except sqlite3.IntegrityError as e:
                if "UNIQUE constraint failed" in str(e):
                    pass
        self.conn.commit()

    def select_article(self):
        return self.cursor.execute(SELECT_ARTICLE_SQL, (self.select_version() + 1,)).fetchall()

    def select_meta(self, meta):
        return self.cursor.execute(SELECT_METADATA_SQL, (meta,)).fetchone()[0]

    def reset_version(self):
        self.insert_meta_data(
            ['VERSION', int(self.cursor.execute(SELECT_LAST_VERION_FROM_ARTICLE_SQL).fetchone()[0]) - 1])

    def select_all_article_id(self):
        return self.cursor.execute(SELECT_ALL_ARTICLE_ID_SQL).fetchall()

# !/usr/bin/env python
# -*- encoding: utf-8 -*-
# vim: set et sw=4 ts=4 sts=4 ff=unix fenc=utf8:
# Author: Vincent<vincent8280@outlook.com>
#         http://wax8280.github.io
# Created on 2017/10/11 12:30
import click
import multiprocessing

from web2kindle.libs.utils import read_file_to_list


@click.group()
def cli():
    pass


@cli.command('zhihu_collection')
@click.option('--i')
@click.option('--f')
@click.option('--start', default=1)
@click.option('--end', default=float('inf'))
@click.option('--img/--no-img', default=True)
def zhihu_collection_main(i, f, start, end, img):
    import web2kindle.script.zhihu_collection
    kw = {}
    kw.update({
        'img': img,
    })
    if i:
        web2kindle.script.zhihu_collection.main([i], start, end, kw)
    elif f:
        collection_list = read_file_to_list(f)
        if isinstance(collection_list, list):
            web2kindle.script.zhihu_collection.main(collection_list, start, end, kw)
        else:
            click.echo(collection_list)


@cli.command('zhihu_zhuanlan')
@click.option('--i')
@click.option('--f')
@click.option('--start', default=1)
@click.option('--end', default=float('inf'))
@click.option('--img/--no-img', default=True)
def zhihu_zhuanlan_main(i, f, start, end, img):
    import web2kindle.script.zhihu_zhuanlan
    kw = {}
    kw.update({
        'img': img,
    })

    if i:
        web2kindle.script.zhihu_zhuanlan.main([i], start, end, kw)
    elif f:
        zhuanlan_list = read_file_to_list(f)
        if isinstance(zhuanlan_list, list):
            web2kindle.script.zhihu_zhuanlan.main(zhuanlan_list, start, end, kw)
        else:
            click.echo(zhuanlan_list)


@cli.command('zhihu_answers')
@click.option('--i')
@click.option('--f')
@click.option('--start', default=1)
@click.option('--end', default=float('inf'))
@click.option('--img/--no-img', default=True)
def zhihu_answers_main(i, f, start, end, img):
    import web2kindle.script.zhihu_answers
    kw = {}
    kw.update({
        'img': img,
    })

    if i:
        web2kindle.script.zhihu_answers.main([i], start, end, kw)
    elif f:
        people_list = read_file_to_list(f)
        if isinstance(people_list, list):
            web2kindle.script.zhihu_answers.main(people_list, start, end, kw)
        else:
            click.echo(people_list)


if __name__ == '__main__':
    multiprocessing.freeze_support()
    cli()

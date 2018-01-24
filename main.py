# !/usr/bin/env python
# -*- encoding: utf-8 -*-
# vim: set et sw=4 ts=4 sts=4 ff=unix fenc=utf8:
# Author: Vincent<vincent8280@outlook.com>
#         http://wax8280.github.io
# Created on 2017/10/11 12:30
import click
import multiprocessing

from web2kindle.script import zhihu_collection_main, zhihu_zhuanlan_main, zhihu_answers_main, guoke_scientific_main, \
    qdaily_main, make_mobi, send_mobi, jianshu_wenji_main, jianshu_zhuanti_main, jianshu_user_main

INF = 999999999


@click.group()
def cli():
    pass


@cli.command('zhihu_collection')
@click.option('--i')
@click.option('--f')
@click.option('--start', default=1)
@click.option('--end', default=INF)
@click.option('--img/--no-img', default=True)
@click.option('--gif/--no-gif', default=False)
@click.option('--email/--no-email', default=False)
@click.option('--window', default=50)
def zhihu_collection_main_cli(i, f, start, end, img, gif, email, window):
    zhihu_collection_main(i, f, start, end, img, gif, email, window=window)


@cli.command('zhihu_zhuanlan')
@click.option('--i')
@click.option('--f')
@click.option('--start', default=1)
@click.option('--end', default=INF)
@click.option('--img/--no-img', default=True)
@click.option('--gif/--no-gif', default=False)
@click.option('--email/--no-email', default=False)
@click.option('--window', default=50)
def zhihu_zhuanlan_main_cli(i, f, start, end, img, gif, email, window):
    zhihu_zhuanlan_main(i, f, start, end, img, gif, email, window=window)


@cli.command('zhihu_answers')
@click.option('--i')
@click.option('--f')
@click.option('--start', default=1)
@click.option('--end', default=INF)
@click.option('--img/--no-img', default=True)
@click.option('--gif/--no-gif', default=False)
@click.option('--email/--no-email', default=False)
@click.option('--window', default=50)
def zhihu_answers_main_cli(i, f, start, end, img, gif, email, window):
    zhihu_answers_main(i, f, start, end, img, gif, email, window=window)


@cli.command('guoke_scientific')
@click.option('--start', default=0)
@click.option('--end', default=INF)
@click.option('--img/--no-img', default=True)
@click.option('--gif/--no-gif', default=False)
@click.option('--email/--no-email', default=False)
@click.option('--window', default=50)
def guoke_scientific_main_cli(start, end, img, gif, email, window):
    guoke_scientific_main(start, end, img, gif, email, window=window)


@cli.command('qdaily')
@click.option('--start', default='default')
@click.option('--i', default='home')
@click.option('--end', default='default')
@click.option('--img/--no-img', default=True)
@click.option('--gif/--no-gif', default=False)
@click.option('--email/--no-email', default=False)
@click.option('--window', default=50)
def qdaily_main_cli(start, end, type, img, gif, email, window):
    qdaily_main(start, end, type, img, gif, email, window=window)


@cli.command('make_mobi')
@click.option('--multi/--single', default=True)
@click.option('--path')
@click.option('--window', default=50)
def make_mobi_cli(path, window, multi):
    make_mobi(path, window, multi)


@cli.command('send_mobi')
@click.option('--path')
def send_mobi_cli(path):
    send_mobi(path)


@cli.command('jianshu_wenji')
@click.option('--i')
@click.option('--f')
@click.option('--start', default=1)
@click.option('--end', default=INF)
@click.option('--img/--no-img', default=True)
@click.option('--gif/--no-gif', default=False)
@click.option('--email/--no-email', default=False)
@click.option('--order_by', default='')
@click.option('--window', default=50)
def jianshu_wenji_cli(i, f, start, end, img, gif, email, order_by, window):
    jianshu_wenji_main(i, f, start, end, img, gif, email, order_by=order_by, window=window)


@cli.command('jianshu_zhuanti')
@click.option('--i')
@click.option('--f')
@click.option('--start', default=1)
@click.option('--end', default=INF)
@click.option('--img/--no-img', default=True)
@click.option('--gif/--no-gif', default=False)
@click.option('--email/--no-email', default=False)
@click.option('--order_by', default='')
@click.option('--window', default=50)
def jianshu_zhuanti_cli(i, f, start, end, img, gif, email, order_by, window):
    jianshu_zhuanti_main(i, f, start, end, img, gif, email, order_by=order_by, window=window)


@cli.command('jianshu_user')
@click.option('--i')
@click.option('--f')
@click.option('--start', default=1)
@click.option('--end', default=INF)
@click.option('--img/--no-img', default=True)
@click.option('--gif/--no-gif', default=False)
@click.option('--email/--no-email', default=False)
@click.option('--order_by', default='')
@click.option('--window', default=50)
def jianshu_user_cli(i, f, start, end, img, gif, email, order_by, window):
    jianshu_user_main(i, f, start, end, img, gif, email, order_by=order_by, window=window)


if __name__ == '__main__':
    multiprocessing.freeze_support()
    cli()

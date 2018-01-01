# !/usr/bin/env python
# -*- encoding: utf-8 -*-
# vim: set et sw=4 ts=4 sts=4 ff=unix fenc=utf8:
# Author: Vincent<vincent8280@outlook.com>
#         http://wax8280.github.io
# Created on 2017/10/11 12:30
import click
import multiprocessing

from web2kindle.libs.utils import read_file_to_list
from web2kindle.script import qdaily, zhihu_collection_main, zhihu_zhuanlan_main, zhihu_answers_main, \
    guoke_scientific_main, qdaily_main, make_mobi, send_mobi


@click.group()
def cli():
    pass


@cli.command('zhihu_collection')
@click.option('--i')
@click.option('--f')
@click.option('--start', default=1)
@click.option('--end', default=float('inf'))
@click.option('--img/--no-img', default=True)
@click.option('--gif/--no-gif', default=False)
@click.option('--email/--no-email', default=False)
def zhihu_collection_main_cli(i, f, start, end, img, gif, email):
    zhihu_collection_main(i, f, start, end, img, gif, email)


@cli.command('zhihu_zhuanlan')
@click.option('--i')
@click.option('--f')
@click.option('--start', default=1)
@click.option('--end', default=float('inf'))
@click.option('--img/--no-img', default=True)
@click.option('--gif/--no-gif', default=False)
@click.option('--email/--no-email', default=False)
def zhihu_zhuanlan_main_cli(i, f, start, end, img, gif, email):
    zhihu_zhuanlan_main(i, f, start, end, img, gif, email)


@cli.command('zhihu_answers')
@click.option('--i')
@click.option('--f')
@click.option('--start', default=1)
@click.option('--end', default=float('inf'))
@click.option('--img/--no-img', default=True)
@click.option('--gif/--no-gif', default=False)
@click.option('--email/--no-email', default=False)
def zhihu_answers_main_cli(i, f, start, end, img, gif, email):
    zhihu_answers_main(i, f, start, end, img, gif, email)


@cli.command('guoke_scientific')
@click.option('--start', default=0)
@click.option('--end', default=float('inf'))
@click.option('--img/--no-img', default=True)
@click.option('--gif/--no-gif', default=False)
@click.option('--email/--no-email', default=False)
def guoke_scientific_main_cli(start, end, img, gif, email):
    guoke_scientific_main(start, end, img, gif, email)


@cli.command('qdaily')
@click.option('--start', default='default')
@click.option('--i', default='home')
@click.option('--end', default='default')
@click.option('--img/--no-img', default=True)
@click.option('--gif/--no-gif', default=False)
@click.option('--email/--no-email', default=False)
def qdaily_main_cli(start, end, type, img, gif, email):
    qdaily_main(start, end, type, img, gif, email)


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


if __name__ == '__main__':
    multiprocessing.freeze_support()
    cli()

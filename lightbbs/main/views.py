# -*- coding:utf-8 -*-
__author__ = 'duwen'

from . import main


@main.route('/', methods=['GET', 'POST'])
def index():
    return 'hi'
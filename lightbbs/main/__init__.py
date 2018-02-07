# -*- coding:utf-8 -*-
__author__ = 'duwen'

from flask import Blueprint

main = Blueprint('main', __name__)

from . import views, errors

# -*- coding:utf-8 -*-
__author__ = 'duwen'

from flask import Blueprint

admin = Blueprint('myadmin', __name__)

from . import views

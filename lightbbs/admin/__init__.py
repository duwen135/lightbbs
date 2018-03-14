# -*- coding:utf-8 -*-
__author__ = 'duwen'

from flask import Blueprint

admin = Blueprint('admin', __name__)

from . import views, forms

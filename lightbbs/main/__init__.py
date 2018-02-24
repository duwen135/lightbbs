# -*- coding:utf-8 -*-
__author__ = 'duwen'

from flask import Blueprint

main = Blueprint('main', __name__)

from . import views, errors
from ..models.role import Permission


@main.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)
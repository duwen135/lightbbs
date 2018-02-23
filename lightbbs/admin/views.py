# -*- coding:utf-8 -*-
__author__ = 'duwen'

from flask import render_template, request, redirect, url_for
from .. import admin
from flask_login import current_user
from flask_admin import Admin, BaseView, expose


class MyView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/index.html')

admin.add_view(MyView(name='Hello 1', endpoint='test1', category='Test'))
admin.add_view(MyView(name='Hello 2', endpoint='test2', category='Test'))
admin.add_view(MyView(name='Hello 3', endpoint='test3', category='Test'))

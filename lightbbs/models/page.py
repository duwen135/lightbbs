# -*- coding:utf-8 -*-
__author__ = 'duwen'

from lightbbs import db


class Page(db.Model):
    __tablename__ = 'lb_pages'
    id = db.Column(db.Integer, unique=True, primary_key=True)
    title = db.Column(db.String(64))
    content = db.Column(db.Text)
    go_url = db.Column(db.String(64))
    add_time = db.Column(db.DateTime)
    is_hidden = db.Column(db.Boolean)

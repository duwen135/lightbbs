# -*- coding:utf-8 -*-
__author__ = 'duwen'

from lightbbs import db
from datetime import datetime


class Page(db.Model):
    __tablename__ = 'lb_pages'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    keywords = db.Column(db.String(64))
    content = db.Column(db.Text)
    go_url = db.Column(db.String(64))
    add_time = db.Column(db.DateTime, default=datetime.utcnow())
    is_hidden = db.Column(db.Boolean)

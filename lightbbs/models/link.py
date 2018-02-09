# -*- coding:utf-8 -*-
__author__ = 'duwen'

from lightbbs import db


class Link(db.Model):
    __tablename__ = 'lb_links'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    url = db.Column(db.String(64))
    logo = db.Column(db.String(64))
    is_hidden = db.Column(db.Boolean)

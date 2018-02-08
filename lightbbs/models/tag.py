# -*- coding:utf-8 -*-
__author__ = 'duwen'

from lightbbs import db


class Tag(db.Model):
    __tablename__ = 'lb_tags'
    id = db.Column(db.Integer, unique=True, primary_key=True)
    tag_title = db.Column(db.String(64))
    topics = db.Column(db.Integer)

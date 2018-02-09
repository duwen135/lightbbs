# -*- coding:utf-8 -*-
__author__ = 'duwen'

from lightbbs import db


class Tag(db.Model):
    __tablename__ = 'lb_tags'
    id = db.Column(db.Integer, primary_key=True)
    tag_name = db.Column(db.String(64))
    topic_num = db.Column(db.Integer)

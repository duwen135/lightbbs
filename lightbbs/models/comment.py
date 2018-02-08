# -*- coding:utf-8 -*-
__author__ = 'duwen'

from lightbbs import db


class Comment(db.Model):
    __tablename__ = 'lb_comments'
    id = db.Column(db.Integer, unique=True, primary_key=True)
    topic_id = db.Column(db.Integer, unique=True)
    uid = db.Column(db.Integer, unique=True)
    content = db.Column(db.Text)
    replytime = db.Column(db.DateTime)
